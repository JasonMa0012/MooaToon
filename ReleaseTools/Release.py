import os
import sys
import subprocess
import datetime
import github_release as ghr
import github3 as gh
from dotenv import load_dotenv
import winreg
import locale
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor


# Inputs: MooaRootDir engineBranchName projectBranchName [--Clean --BuildEngine --ZipEngine --ZipProject --Release --Reupload]

# ================= Defines =================
repo_name = "JasonMa0012/MooaToon"

mooatoon_root_path = r"E:\MooaRel"
if len(sys.argv) > 1:
    mooatoon_root_path = sys.argv[1]

engine_version = "5.6"
if len(sys.argv) > 2:
    engine_version = sys.argv[2]

project_branch_name = "5.6_MooaToonProject"
if len(sys.argv) > 3:
    project_branch_name = sys.argv[3]

# Default Input
argv = [
    '--Release'
    # '--Reupload'
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


def upload_single_asset(repo_name, tag_name, file_path, lock):
    """上传单个文件的线程函数，失败时无限重试"""
    file_name = os.path.basename(file_path)
    retry_count = 0
    
    with lock:
        print(f"开始上传: {file_name}")
    
    while True:
        try:
            ghr.gh_asset_upload(repo_name, tag_name, [file_path])
            
            with lock:
                if retry_count > 0:
                    print(f"上传成功: {file_name} (重试 {retry_count} 次后成功)")
                else:
                    print(f"上传成功: {file_name}")
            return True
            
        except Exception as e:
            retry_count += 1
            with lock:
                print(f"上传失败: {file_name}, 错误: {str(e)}")
                print(f"第 {retry_count} 次重试中... (3秒后重试)")
            
            # 等待3秒后重试
            time.sleep(3)


def multithread_upload(repo_name, tag_name, file_paths):
    """多线程上传文件，每个文件都会重试直到成功"""
    if not file_paths:
        print("没有文件需要上传")
        return True
    
    # 计算并发线程数：文件总数的1/3，但至少1个
    max_workers = max(1, len(file_paths) // 3)
    
    print(f"开始多线程上传 {len(file_paths)} 个文件...")
    print(f"同时上传文件数量: {max_workers} (文件总数的1/3)")
    print("注意: 每个文件都会重试直到上传成功")
    
    lock = threading.Lock()
    
    # 使用线程池控制并发数量
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有上传任务
        futures = []
        for file_path in file_paths:
            future = executor.submit(upload_single_asset, repo_name, tag_name, file_path, lock)
            futures.append(future)
        
        # 等待所有任务完成
        for future in futures:
            future.result()  # 这会等待任务完成，如果有异常会抛出
    
    with lock:
        print(f"所有文件上传完成: {len(file_paths)} 个文件全部上传成功")
    
    return True  # 现在总是返回True，因为会无限重试直到成功


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
    # https://www.bandisoft.com/bandizip/help/parameter/
    args = [bandizip_path, "a", "-l:9", "-y", "-v:2000MB", "-t:120", engine_zip_path, engine_path + r"\LocalBuilds\Engine", ]
    async_run(args)

if '--ZipProject' in argv:
    print("======Zip Project======")
    args = [bandizip_path, "a", "-l:9", "-y", "-v:2000MB", "-t:120", project_zip_path,
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

    # Compose compare link (English) and enforce GitHub body length limit (125000)
    MAX_BODY = 100000
    compare_section = ""
    if last_release_info is not None:
        prev_tag = last_release_info['tag_name']
        compare_url = f"https://github.com/{repo_name}/compare/{prev_tag}...{release_name}"
        compare_section = f"\n\n**Full Changelog**:\n{compare_url}\n"
    else:
        compare_section = ""

    if comment is None:
        comment = ""

    # Ensure the final body keeps the compare link while respecting the max length
    reserved = len(compare_section)
    if len(comment) + reserved > MAX_BODY:
        notice = "\n\n(Commit list truncated due to length limit)\n"
        allowed = MAX_BODY - reserved - len(notice)
        if allowed < 0:
            allowed = 0
        comment = comment[:allowed] + notice

    final_body = comment + compare_section

    try:
        ghr.gh_release_create(
            repo_name,
            release_name,
            publish=False,
            body=final_body,
            name=release_name,
        )
    except Exception as e:
        if isinstance(e, requests.HTTPError) and e.response is not None:
            print("Create release failed:", e.response.status_code, e.response.reason)
            try:
                print("Details:", e.response.json())
            except Exception:
                print("Raw:", e.response.text[:1000])
        raise

    # 使用多线程上传
    upload_success = multithread_upload(repo_name, release_name, file_paths)
    if upload_success:
        ghr.gh_release_publish(repo_name, release_name)
    else:
        print("部分文件上传失败，请检查后重试")

if '--Reupload' in argv:
    print("======Reupload======")
    if last_draft_info is not None:
        # 仅上传失败的文件
        for asset in last_draft_info['assets']:
            for file_path in file_paths[:]:  # 使用副本避免在迭代时修改列表
                if file_path.endswith(asset['name']):
                    file_paths.remove(file_path)

        # 使用多线程上传
        upload_success = multithread_upload(repo_name, last_draft_info['tag_name'], file_paths)
        if upload_success:
            ghr.gh_release_publish(repo_name, last_draft_info['tag_name'])
        else:
            print("部分文件上传失败，请检查后重试")
    else:
        print("\nThere is no draft!\n")

input("\nPress Enter to continue...")