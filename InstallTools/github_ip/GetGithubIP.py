'''
Title: 快速获Github网站的IP地址
Author: JackieZheng
Date: 2022-01-20 19:37:35
LastEditTime: 2022-01-22 09:14:49
LastEditors: Please set LastEditors
Description:
FilePath: \\vsTemp\\gitdns.py
'''
import os
import re
import shutil
import requests
import ping3

# to pack exe:
# cmd: C:\Users\13121\AppData\Local\Programs\Python\Python311\python.exe -m PyInstaller -F GetGithubIP.py

hosts_datas = []
git_ip = []
query_url = "https://www.ipaddress.com/site/"
header = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/108.0.0.0'}

def getip(website: str):
    """
    # 获取最快的IP地址
    """
    request = requests.get(query_url + website, headers=header)
    if request.status_code == 200:
        ips = re.findall(r"<strong>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}?)</strong>", request.text)

        FastIp = ""
        PingTime = 0.0
        MinTime = 999.0
        for ip_item in ips:
            PingTime = ping3.ping(ip_item, timeout=1, unit='ms')
            if not PingTime:
                PingTime = 5000.0
            if PingTime < MinTime:
                MinTime = PingTime
                FastIp = ip_item
        print(FastIp + ' ' + website + ' ' + str(int(MinTime)) + 'ms')
        git_ip.append(FastIp + ' ' + website)


getip('github.com')
getip('assets-cdn.github.com')
getip('github.global.ssl.fastly.net')
getip('raw.githubusercontent.com')
getip('gist.githubusercontent.com')
getip('cloud.githubusercontent.com')
getip('camo.githubusercontent.com')
# TODO: add epic IP for Setup.bat


if len(git_ip) == 0:
    print("Failed to query IPs from:" + query_url)
    os.system('timeout /t 5')
    exit()


hosts_dir = os.path.join(os.path.dirname(os.getenv('DRIVERDATA')), 'etc')
temp_hosts_dir = os.getcwd()
orign_hosts = os.path.join(hosts_dir, 'hosts')
temp_hosts = os.path.join(temp_hosts_dir, 'hosts')

# 读取原来hosts内容
with open(orign_hosts, 'r', encoding='utf-8') as orign_file:
    datas = orign_file.readlines()

# 复制hosts内容
hosts_datas = datas.copy()

# 删除原来github相关内容
for data in datas:
    if 'github' in data or data == '\n':
        hosts_datas.remove(data)

# 合并生成新hosts内容
hosts_datas.extend(git_ip)

# 生成临时hosts文件
with open(temp_hosts, 'w') as temp_file:
    for host in hosts_datas:
        temp_file.writelines(host + '\n')


try:
    # 备份 覆盖 系统hosts文件
    shutil.move(orign_hosts, orign_hosts + '.bak')
    shutil.copy(temp_hosts, orign_hosts)
    INFOR_0 = orign_hosts + " Updated!"
    print(INFOR_0)
except:
    # 打开系统hosts目录手动覆盖
    os.system("explorer.exe %s" % hosts_dir)
    os.system("explorer.exe %s" % temp_hosts_dir)
    INFOR_1 = "A new hosts file has been generated: " + temp_hosts
    INFOR_2 = "Please manually copy and override the original system hosts file!\n" \
              "Or you can close the program and reopen it with administrator privileges!"
    print(INFOR_1, INFOR_2, sep='\n')
    INFOR_3 = "\n\nPlease enter any key after overriding!"
    print(INFOR_3)

    os.system('pause')

os.remove(temp_hosts)

# 刷新dns缓存
os.system('ipconfig /flushdns')

print("Github IP Refresh Successfully.")
#os.system('timeout /t 5')