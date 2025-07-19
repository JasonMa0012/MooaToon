import os
import sys
import subprocess
import requests
import github_release as ghr
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


# ================= Defines =================
engine_version = "5.6"
repo_name = "JasonMa0012/MooaToon"
mooatoon_root_path = r"E:\MooaToon"
max_concurrent_downloads = 5

if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]
if len(sys.argv) > 2:
    engine_version = sys.argv[2]
if len(sys.argv) > 3:
    max_concurrent_downloads = int(sys.argv[3])

bandizip_path = os.path.join(mooatoon_root_path, r"InstallationTools\BANDIZIP-PORTABLE\Bandizip.x64.exe")
download_path = os.path.join(mooatoon_root_path, r"InstallationTools\Download")
engine_zip_prefix = "MooaToon-Engine-Precompiled"
project_zip_prefix = "MooaToon-Project-Precompiled"
engine_unzip_path = os.path.join(mooatoon_root_path, engine_zip_prefix)
project_unzip_path = os.path.join(mooatoon_root_path, project_zip_prefix)
clear_engine_whitelist = [
    os.path.join(engine_unzip_path, r"Windows\Engine\Plugins\MooaToon\Content"),
]


if not os.path.exists(download_path):
    os.makedirs(download_path)
if not os.path.exists(engine_unzip_path):
    os.makedirs(engine_unzip_path)
if not os.path.exists(project_unzip_path):
    os.makedirs(project_unzip_path)


# ============ Functions ==============
def async_run(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        if process.stdout is not None:
            output = process.stdout.readline()
        else:
            output = ''
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()


def download_file(url, output_path, file_size, progress_data, lock):
    try:
        headers = {'Accept': 'application/octet-stream'}
        response = requests.get(url, headers=headers, stream=True)

        if os.path.exists(output_path):
            os.remove(output_path)

        block_size = 1024
        downloaded = 0
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(block_size):
                f.write(chunk)
                downloaded += len(chunk)
                with lock:
                    progress_data[output_path]['downloaded'] = downloaded
        
    except requests.exceptions.RequestException as e:
        raise e


def download_with_retry(url, output_path, file_size, progress_data, lock):
    while True:
        try:
            download_file(url, output_path, file_size, progress_data, lock)
            if os.path.exists(output_path) and os.path.getsize(output_path) == file_size:
                break
        except requests.exceptions.RequestException as e:
            print(f"\nError downloading file: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            time.sleep(1)


def get_asset_info(releases, pattern):
    assets = []
    for asset in releases['assets']:
        if pattern in asset['name']:
            assets.append((asset['browser_download_url'], asset['size']))
    return assets


def remove_unwanted_files(download_path, release_files):
    for file_name in os.listdir(download_path):
        if file_name not in release_files:
            file_path = os.path.join(download_path, file_name)
            os.remove(file_path)
            print(f"Deleted: {file_path}")


def delete_files_in_directory(directory, whitelist):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_path in whitelist:
            continue
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_files_in_directory(file_path, whitelist)
            os.rmdir(file_path)


def download_releases(release_info, file_name_prefix, download_path):
    zip_path = ""
    to_download = []
    assets = get_asset_info(release_info, file_name_prefix)
    for url, file_size in assets:
        file_name = url.split('/')[-1]
        output_path = os.path.join(download_path, file_name)
        if output_path.endswith(".zip"):
            zip_path = output_path

        if os.path.exists(output_path) and os.path.getsize(output_path) == file_size:
            print(f"\nSkipping {file_name}, file already exists with the same size.")
        else:
            to_download.append((url, output_path, file_size))

    if to_download:
        progress_data = {}
        lock = threading.Lock()
        for url, output_path, file_size in to_download:
            progress_data[output_path] = {'downloaded': 0, 'file_size': file_size, 'done': False}

        def monitor_progress(release_info):
            prev_downloaded = {path: 0 for path in progress_data}
            prev_time = time.time()
            
            while True:
                time.sleep(1)
                with lock:
                    current_time = time.time()
                    delta_time = current_time - prev_time
                    if delta_time <= 0:
                        continue

                    # 清屏并回到顶部
                    import os
                    if os.name == 'nt':  # Windows
                        os.system('cls')
                    else:  # Unix/Linux/Mac
                        os.system('clear')
                    
                    # 置顶显示 Release 信息
                    print_release_info(release_info)
                    
                    print("======Download Progress======\n")
                    
                    total_delta = 0
                    waiting_files = []
                    active_downloads = []
                    
                    for url, output_path, file_size in to_download:
                        if output_path in progress_data:
                            data = progress_data[output_path]
                            dl = data['downloaded']
                            size = data['file_size']
                            prog = (dl / size * 100) if size > 0 else 0
                            delta_dl = dl - prev_downloaded[output_path]
                            speed = delta_dl / (1024 * 1024 * delta_time) if delta_time > 0 else 0
                            prev_downloaded[output_path] = dl
                            total_delta += delta_dl
                            
                            # 只显示正在下载的文件（进度大于0%且小于100%）
                            if 0 < prog < 100:
                                active_downloads.append({
                                    'file_name': os.path.basename(output_path),
                                    'url': url,
                                    'progress': prog,
                                    'speed': speed
                                })
                            elif prog == 0:
                                # 收集等待下载的文件
                                waiting_files.append(os.path.basename(output_path))
                    
                    # 显示正在下载的文件
                    for download in active_downloads:
                        print(f"File: {download['file_name']}")
                        print(f"URL: {download['url']}")
                        progress_bar = "█" * int(download['progress'] // 2) + "░" * (50 - int(download['progress'] // 2))
                        print(f"Progress: [{progress_bar}] {download['progress']:.2f}% - {download['speed']:.2f}MB/s")
                        print()
                        print()

                    total_speed = total_delta / (1024 * 1024 * delta_time) if delta_time > 0 else 0
                    print(f"Total download speed: {total_speed:.2f}MB/s")
                    
                    # 显示等待下载的文件列表
                    if waiting_files:
                        print()
                        print(f"{len(waiting_files)} files waiting to download:")
                        for file_name in waiting_files:
                            print(f"- {file_name}")

                    prev_time = current_time

                    if all(d['done'] for d in progress_data.values()):
                        print("\nAll downloads completed!\n")
                        break

        monitor_thread = threading.Thread(target=monitor_progress, args=(release_info,))
        monitor_thread.start()
        print("\nDownloading progress:\n")

        def download_task(url, output_path, file_size, progress_data, lock):
            download_with_retry(url, output_path, file_size, progress_data, lock)
            with lock:
                progress_data[output_path]['done'] = True

        with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
            futures = [executor.submit(download_task, url, output_path, file_size, progress_data, lock) for url, output_path, file_size in to_download]
            for future in as_completed(futures):
                future.result()

        monitor_thread.join()

    return zip_path


def print_release_info(release_info):
    print("===================================================================\n")
    print(f"Latest Release: {release_info['name']} ({release_info['html_url']})")
    print()
    print("Release Notes:")
    print(release_info['body'])
    print("\n===================================================================\n")


# ================= Main ==================
latest_release_info = None
for release in ghr.get_releases(repo_name):
    if (not release['prerelease']) and (not release['draft']) and (release["tag_name"].startswith(engine_version)):
        latest_release_info = release
        break

if latest_release_info == None :
    input(f"\nCant not find {engine_version} release! \nMake sure your network has access to github.com and that _2_5_Settings.bat settings are correct! \n\nPress Enter to continue...")
    exit(1)

print_release_info(latest_release_info)

release_files = []
for asset in latest_release_info['assets']:
    release_files.append(asset['name'])

print("\n\n======Clear======")
remove_unwanted_files(download_path, release_files)

print("\n\n======Download Engine======")
engine_zip_path = download_releases(latest_release_info, engine_zip_prefix, download_path)

print("\n\n======Download Project======")
project_zip_path = download_releases(latest_release_info, project_zip_prefix, download_path)

print("\n\n======Clear Engine======")
delete_files_in_directory(engine_unzip_path, clear_engine_whitelist)

print("\n\n======Unzip Engine======")
args = [bandizip_path, "x", "-aoa", "-y", "-o:" + engine_unzip_path, engine_zip_path]
async_run(args)

print("\n\n======Unzip Project======")
args = [bandizip_path, "x", "-aoa", "-y", "-o:" + project_unzip_path, project_zip_path]
async_run(args)

print("\n\n======Installation Completed======")
input("\nPress Enter to continue...")

