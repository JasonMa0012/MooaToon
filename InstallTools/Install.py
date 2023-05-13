import os
import sys
import subprocess
import github_release as ghr

repo_name = "JasonMa0012/MooaToon"
mooatoon_root_path = r"X:\MooaToon"
if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]

argv = [
    '--Clean',
    '--DownloadEngine',
    '--DownloadProject',
    '--UnzipEngine',
    '--UnzipProject',
]
if len(sys.argv) > 2:
    argv = sys.argv[2:]

bandizip_path = mooatoon_root_path + r"\InstallTools\BANDIZIP-PORTABLE\Bandizip.x64.exe"
download_path = mooatoon_root_path + r"\InstallTools\Download"
engine_zip_name = "MooaToon-Engine-Precompiled"
project_zip_name = "MooaToon-Project-Precompiled"
engine_zip_path = download_path + "\\" + engine_zip_name + ".zip"
project_zip_path = download_path + "\\" + project_zip_name + ".zip"
engine_unzip_path = mooatoon_root_path + "\\" + engine_zip_name
project_unzip_path = mooatoon_root_path + "\\" + project_zip_name


def AsyncRun(args):
    # 使用 subprocess.Popen() 函数异步执行 bat 文件，并获取 stdout 和 stderr 输出
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()


latest_release_info = ghr.get_releases(repo_name)[0]
tag_name = latest_release_info['tag_name']

if not os.path.exists(download_path):
    os.makedirs(download_path)
if not os.path.exists(engine_unzip_path):
    os.makedirs(engine_unzip_path)
if not os.path.exists(project_unzip_path):
    os.makedirs(project_unzip_path)

if '--Clean' in argv:
    print("======Clean======")
    for file_name in os.listdir(download_path):
        file_path = os.path.join(download_path, file_name)
        os.remove(file_path)
        print(file_path)

if '--DownloadEngine' in argv:
    print("======Download Engine======")
    os.chdir(download_path)
    ghr.gh_asset_download(repo_name, tag_name, engine_zip_name + ".*")

if '--DownloadProject' in argv:
    print("======Download Project======")
    os.chdir(download_path)
    ghr.gh_asset_download(repo_name, tag_name, project_zip_name + ".*")

if '--UnzipEngine' in argv:
    print("======Unzip Engine======")
    args = [bandizip_path, "x", "-aoa", "-y", "-o:" + engine_unzip_path, engine_zip_path]
    AsyncRun(args)

if '--UnzipProject' in argv:
    print("======Unzip Project======")
    args = [bandizip_path, "x", "-aoa", "-y", "-o:" + project_unzip_path, project_zip_path]
    AsyncRun(args)


print("======Installation Completed======")
