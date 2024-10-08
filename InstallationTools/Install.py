import os
import sys
import subprocess
import requests
import github_release as ghr
import time


# ================= Defines =================
engine_version = "5.3"
repo_name = "JasonMa0012/MooaToon"
mooatoon_root_path = r"X:\MooaToon"

if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]
if len(sys.argv) > 2:
    engine_version = sys.argv[2]

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


# ================= Main ==================
latest_release_info = None
for release in ghr.get_releases(repo_name):
    if (not release['prerelease']) and (not release['draft']) and (release["tag_name"].startswith(engine_version)):
        latest_release_info = release
        break

if latest_release_info == None :
    input(f"\nCant not find {engine_version} release! \nMake sure your network has access to github.com and that _2_5_Settings.bat settings are correct! \n\nPress Enter to continue...")
    exit(1)

print("\n=============================================\n")
print(f"Latest {engine_version} Release: {latest_release_info['tag_name']} ({latest_release_info['html_url']})")
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

