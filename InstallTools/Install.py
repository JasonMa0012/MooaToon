import os
import sys
import subprocess
import requests
import github_release as ghr
import time


def AsyncRun(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()


def download_file(url, output_path, file_size):
    try:
        headers = {'Accept': 'application/octet-stream'}
        response = requests.get(url, headers=headers, stream=True)

        if os.path.exists(output_path):
            os.remove(output_path)

        block_size = 1024
        downloaded = 0
        start_time = time.time()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(block_size):
                f.write(chunk)
                downloaded += len(chunk)
                elapsed = max(1e-6, time.time() - start_time)
                progress = int(50 * downloaded / file_size)
                speed = downloaded / (1024 * 1024 * elapsed)
                sys.stdout.write(
                    f"\r[{'=' * progress}{' ' * (50 - progress)}] {progress * 2}% {speed:.2f}MB/s")
                sys.stdout.flush()
        print()
    except requests.exceptions.RequestException as e:
        print(f"\nError downloading file: {e}")
        sys.exit(1)


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


def download_releases(release_info, file_name_prefix, download_path):
    zip_path = ""
    assets = get_asset_info(release_info, file_name_prefix)
    for url, file_size in assets:
        file_name = url.split('/')[-1]
        output_path = os.path.join(download_path, file_name)
        if output_path.endswith(".zip"):
            zip_path = output_path

        if os.path.exists(output_path) and os.path.getsize(output_path) == file_size:
            print(f"\nSkipping {file_name}, file already exists with the same size.")
        else:
            while (not os.path.exists(output_path)) or os.path.getsize(output_path) != file_size:
                print(f"\nDownloading {file_name} ({url}) ...")
                download_file(url, output_path, file_size)

    return zip_path


repo_name = "JasonMa0012/MooaToon"
mooatoon_root_path = r"X:\MooaToon"

if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]

bandizip_path = mooatoon_root_path + r"\InstallTools\BANDIZIP-PORTABLE\Bandizip.x64.exe"
download_path = mooatoon_root_path + r"\InstallTools\Download"
engine_zip_prefix = "MooaToon-Engine-Precompiled"
project_zip_prefix = "MooaToon-Project-Precompiled"
engine_unzip_path = mooatoon_root_path + "\\" + engine_zip_prefix
project_unzip_path = mooatoon_root_path + "\\" + project_zip_prefix


if not os.path.exists(download_path):
    os.makedirs(download_path)
if not os.path.exists(engine_unzip_path):
    os.makedirs(engine_unzip_path)
if not os.path.exists(project_unzip_path):
    os.makedirs(project_unzip_path)


latest_release_info = None
for release in ghr.get_releases(repo_name):
    if (not release['prerelease']) and (not release['draft']):
        latest_release_info = release
        break

print("\n=============================================\n")
print(f"Latest Release: {latest_release_info['tag_name']} ({latest_release_info['html_url']})")
print("\n=============================================\n")

release_files = []
for asset in latest_release_info['assets']:
    release_files.append(asset['name'])

print("\n\n======Clear======")
remove_unwanted_files(download_path, release_files)

print("\n\n======Download Engine======")
engine_zip_path = download_releases(latest_release_info, engine_zip_prefix, download_path)

print("\n\n======Download Project======")
project_zip_path = download_releases(latest_release_info, project_zip_prefix, download_path)

print("\n\n======Unzip Engine======")
args = [bandizip_path, "x", "-aoa", "-y", "-o:" + engine_unzip_path, engine_zip_path]
AsyncRun(args)

print("\n\n======Unzip Project======")
args = [bandizip_path, "x", "-aoa", "-y", "-o:" + project_unzip_path, project_zip_path]
AsyncRun(args)

print("\n\n======Installation Completed======")
input("\nPress Enter to continue...")