import os
import sys
import subprocess
import datetime
import github_release as ghr
import github3 as gh
from dotenv import load_dotenv
import winreg
import locale


# Inputs: MooaRootDir engineBranchName projectBranchName [--Clean --BuildEngine --ZipEngine --ZipProject --Release --Reupload]

# ================= Defines =================
repo_name = "JasonMa0012/MooaToon"

mooatoon_root_path = r"X:\MooaToon"
if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]

engine_version = "5.5"
if len(sys.argv) > 2:
    engine_version = sys.argv[2]

project_branch_name = "5.5_MooaToonProject"
if len(sys.argv) > 3:
    project_branch_name = sys.argv[3]

# Default Input
argv = [
    '--Reupload'
]
if len(sys.argv) > 4:
    argv = sys.argv[4:]

current_date = datetime.date.today().strftime("%Y.%m.%d")
release_name = engine_version + "-" + current_date

bandizip_path = mooatoon_root_path + r"\InstallationTools\BANDIZIP-PORTABLE\Bandizip.x64.exe"
zip_path = mooatoon_root_path + r"\ReleaseTools\Zip"
engine_path = mooatoon_root_path + r"\MooaToon-Engine"
project_path = mooatoon_root_path + r"\MooaToon-Project"
engine_zip_path = zip_path + r"\MooaToon-Engine-Precompiled-" + release_name + ".zip"
project_zip_path = zip_path + r"\MooaToon-Project-Precompiled-" + release_name + ".zip"

engine_user = 'Jason-Ma-0012'
engine_repo = 'MooaToon-Engine'


if not os.path.exists(zip_path):
    os.makedirs(zip_path)


# ============ Functions ==============
def get_onedrive_env_path():
    # 打开 OneDrive 注册表项
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\OneDrive", 0, winreg.KEY_READ) as key:
        # 获取 OneDrive 安装路径的值
        envPath, _ = winreg.QueryValueEx(key, "UserFolder")

    return os.path.join(envPath, '_Data', 'envs', 'MooaToon.env')


def get_release_comment(branch_name, last_release_date):
    g = gh.login(token=os.getenv('MOOATOON_ENGINE_TOKEN'))
    repo : gh.github.repo.Repository = g.repository(engine_user, engine_repo)
    comment = ''
    for commit in repo.commits(sha=branch_name, since=last_release_date):
        comment += f'\n[[{commit.sha[0:7]}]({commit.html_url})]\n'
        comment += commit.message
        comment += '\n'
    return comment


def async_run(args):
    # 获取系统的默认编码
    encoding = locale.getpreferredencoding()
    # 使用 subprocess.Popen() 函数异步执行 bat 文件，并获取 stdout 和 stderr 输出
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding=encoding, errors='ignore')

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()


# ================= Main ==================
load_dotenv(dotenv_path=get_onedrive_env_path())

if '--Clean' in argv:
    print("======Clean======")
    for file_name in os.listdir(zip_path):
        file_path = os.path.join(zip_path, file_name)
        os.remove(file_path)
        print(file_path)

if '--BuildEngine' in argv:
    print("======Build Engine======")
    os.chdir(engine_path)
    async_run([engine_path + r"\_build.bat"])

if '--ZipEngine' in argv:
    print("======Zip Engine======")
    args = [bandizip_path, "a", "-l:9", "-y", "-v:2000MB", "-t:60", engine_zip_path, engine_path + r"\LocalBuilds\Engine", ]
    async_run(args)

if '--ZipProject' in argv:
    print("======Zip Project======")
    args = [bandizip_path, "a", "-l:9", "-y", "-v:2000MB", "-t:60", project_zip_path,
            project_path + r"\Art",
            project_path + r"\Config",
            project_path + r"\Content",
            project_path + r"\Plugins",
            project_path + r"\MooaToon_Project.uproject", ]
    async_run(args)

file_paths = []
for file_name in os.listdir(zip_path):
    file_path = os.path.join(zip_path, file_name)
    file_paths.append(file_path)

last_release_info = None
last_draft_info = None
for release in ghr.get_releases(repo_name):
    if release['draft']:
        last_draft_info = release
    elif release['tag_name'].startswith(engine_version):
        last_release_info = release
        break

if '--Release' in argv:
    print("======Release======")
    if last_release_info is None:
        comment = "No Messages."
    else:
        comment = get_release_comment(engine_version, last_release_info['published_at'][0:10])
        comment += get_release_comment(project_branch_name, last_release_info['published_at'][0:10])
    ghr.gh_release_create(
        repo_name,
        release_name,
        publish=False,
        body=comment,
        name=release_name,
        asset_pattern=file_paths,
    )
    ghr.gh_release_publish(repo_name, release_name)

if '--Reupload' in argv:
    print("======Reupload======")
    if last_draft_info is not None:
        # 仅上传失败的文件
        for asset in last_draft_info['assets']:
            for file_path in file_paths:
                if file_path.endswith(asset['name']):
                    file_paths.remove(file_path)

        ghr.gh_asset_upload(repo_name, last_draft_info['tag_name'], file_paths)
        ghr.gh_release_publish(repo_name, last_draft_info['tag_name'])
    else:
        print("\nThere is no draft!\n")

input("\nPress Enter to continue...")