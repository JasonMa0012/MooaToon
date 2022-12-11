import requests
from bs4 import BeautifulSoup
import os
import subprocess

class gitip:
    def __init__(self, ip_list):
        super().__init__()
        self.ip_list = ip_list
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        self.ip_1 = 'https://github.com.ipaddress.com/' # github.com
        self.ip_2 = 'https://github.com.ipaddress.com/gist.github.com' # gist.github.com
        self.ip_3 = 'https://github.com.ipaddress.com/assets-cdn.github.com' # assets-cdn.github.com
        self.ip_4 = 'https://site.ip138.com/raw.githubusercontent.com/' # raw.githubusercontent.com
    def get_1(self): # github.com
        response = requests.get(self.ip_1, headers = self.header)
        soup = BeautifulSoup(response.text, features = 'lxml')
        # print(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    github.com')
        self.ip_list.append(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    github.com')
    def get_2(self):
        response = requests.get(self.ip_2, headers = self.header)
        soup = BeautifulSoup(response.text, features = 'lxml')
        # print(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    gist.github.com')
        self.ip_list.append(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    gist.github.com')
    def get_3(self):
        response = requests.get(self.ip_3, headers = self.header)
        soup = BeautifulSoup(response.text, features = 'lxml')
        ips = soup.find_all('li')
        for i in range(4):
            # print(ips[i].text + '    assets-cdn.github.com')
            self.ip_list.append(ips[i].text + '    assets-cdn.github.com')
    def get_4(self):
        response = requests.get(self.ip_4, headers = self.header)
        soup = BeautifulSoup(response.text, features = 'lxml')
        # print(soup.find_all('a', {'target': '_blank'})[26].text + '    raw.githubusercontent.com')
        ip = soup.find_all('a', {'target': '_blank'})[25].text
        # print(ip + '    raw.githubusercontent.com')
        # print(ip + '    gist.githubusercontent.com')
        # print(ip + '    cloud.githubusercontent.com')
        # print(ip + '    camo.githubusercontent.com')
        # print(ip + '    avatars0.githubusercontent.com')
        # print(ip + '    avatars1.githubusercontent.com')
        # print(ip + '    avatars2.githubusercontent.com')
        # print(ip + '    avatars3.githubusercontent.com')
        # print(ip + '    avatars4.githubusercontent.com')
        # print(ip + '    avatars5.githubusercontent.com')
        # print(ip + '    avatars6.githubusercontent.com')
        # print(ip + '    avatars7.githubusercontent.com')
        # print(ip + '    avatars8.githubusercontent.com')
        self.ip_list.append(ip + '    raw.githubusercontent.com')
        self.ip_list.append(ip + '    gist.githubusercontent.com')
        self.ip_list.append(ip + '    cloud.githubusercontent.com')
        self.ip_list.append(ip + '    camo.githubusercontent.com')
        self.ip_list.append(ip + '    avatars0.githubusercontent.com')
        self.ip_list.append(ip + '    avatars1.githubusercontent.com')
        self.ip_list.append(ip + '    avatars2.githubusercontent.com')
        self.ip_list.append(ip + '    avatars3.githubusercontent.com')
        self.ip_list.append(ip + '    avatars4.githubusercontent.com')
        self.ip_list.append(ip + '    avatars5.githubusercontent.com')
        self.ip_list.append(ip + '    avatars6.githubusercontent.com')
        self.ip_list.append(ip + '    avatars7.githubusercontent.com')
        self.ip_list.append(ip + '    avatars8.githubusercontent.com')

if __name__ == '__main__':
    ip_list = []
    error = 0
    github = gitip(ip_list)
    try:
        github.get_1()
    except:
        print('github.com 申请出错')
        error+=1
    try:
        github.get_2()
    except:
        print('gist.github.com 申请出错')
        error+=1
    try:
        github.get_3()
    except:
        print('assets-cdn.github.com 申请出错')
        error+=1
    try:
        github.get_4()
    except:
        print('raw.githubusercontent.com 申请出错')
        error+=1
    # print(github.ip_list)
    if error == 0:
        for i in github.ip_list:
            print(i)
        try:
            subprocess.run("explorer.exe %s" % 'C:\Windows\System32\drivers\etc')
        except:
            print('请打开文件路径 C:\Windows\System32\drivers\etc 更改hosts文件')
    os.system('pause')