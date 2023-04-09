import os
import sys
import subprocess
import io
import datetime
import github_release as ghr

ue_version = "5.1"
repo_name = "JasonMa0012/MooaToon"
mooatoon_root_path = r"X:\MooaToon"
if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]

argv = [
    '--Reupload'
]
if len(sys.argv) > 2:
    argv = sys.argv[2:]

bandizip_path = mooatoon_root_path + r"\InstallTools\BANDIZIP-PORTABLE\Bandizip.x64.exe"
zip_path = mooatoon_root_path + r"\ReleaseTools\Zip"
engine_path = mooatoon_root_path + r"\MooaToon-Engine"
project_path = mooatoon_root_path + r"\MooaToon-Project"
engine_target_path = zip_path + r"\MooaToon-Engine-Precompiled"
project_target_path = zip_path + r"\MooaToon-Project-Precompiled"


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


if '--Clean' in argv:
    print("======Clean======")
    for file_name in os.listdir(zip_path):
        file_path = os.path.join(zip_path, file_name)
        os.remove(file_path)
        print(file_path)

if '--BuildEngine' in argv:
    print("======Build Engine======")
    os.chdir(engine_path)
    AsyncRun([engine_path + r"\_build.bat"])

if '--CleanEngine' in argv:
    print("======Clean Engine======")
    AsyncRun([engine_path + r"\_clean.bat"])

if '--ZipEngine' in argv:
    print("======Zip Engine======")
    args = [bandizip_path, "a", "-l:9", "-y", "-v:2000MB", "-t:60", engine_target_path, engine_path + r"\LocalBuilds\Engine",]
    AsyncRun(args)

if '--ZipProject' in argv:
    print("======Zip Project======")
    args = [bandizip_path, "a", "-l:9", "-y", "-v:2000MB", "-t:60", project_target_path,
            project_path + r"\Art",
            project_path + r"\Content",
            project_path + r"\MooaToon_Project.uproject",]
    AsyncRun(args)


current_date = datetime.date.today().strftime("%Y.%m.%d")
file_paths = []
for file_name in os.listdir(zip_path):
    file_path = os.path.join(zip_path, file_name)
    file_paths.append(file_path)

if '--Release' in argv:
    print("======Release======")
    ghr.gh_release_create(
        repo_name,
        current_date,
        publish=True,
        name=current_date,
        asset_pattern=file_paths,
    )

if '--Reupload' in argv:
    print("======Reupload======")
    release_info = ghr.get_release_info(repo_name, current_date)

    # 仅上传失败的文件
    for asset in release_info['assets']:
        if any(file.endswith(asset['name']) for file in file_paths):
            file_paths.remove(asset['name'])

    ghr.gh_asset_upload(repo_name, current_date, file_paths)


print("Press any key to continue...")
input()