# Github访问速度慢的解决方法

# 说明
由于GitHub收到DNS污染，常常会无法登陆、访问速度慢。
可以采用网络上的一些方法，更改hosts。
但是GitHub的IP地址时不时会发生变化，使用ping有时又ping不通。单独查询每个IP地址又很麻烦。
故此使用python爬虫进行批量查询。
# 实现过程
 1.通过https://www.ipaddress.com 可以查询到一系列GitHub网址的IP。通过开发者工具可以得到IP地址在网页中的位置。
![ipaddress](https://img-blog.csdnimg.cn/20200716105113649.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70)
2.使用python爬虫进行批量请求，将获得的IP地址保存下来。

代码请看代码库中的py文件夹。

* *注：其中raw.githubusercontent.com这个网址在https://www.ipaddress.com 也无法查出IP地址，故转用https://site.ip138.com/ 。*

3.当查询结束之后，程序将自动打开文件路径 C:\Windows\System32\drivers\etc 。

```python
 try:
 	subprocess.run("explorer.exe %s" % 'C:\Windows\System32\drivers\etc')
 except:
 	print('请打开文件路径 C:\Windows\System32\drivers\etc 更改hosts文件')
```

此时只需更改这个目录下的hosts文件即可。(在hosts文件末尾添加)
![hosts文件](https://img-blog.csdnimg.cn/20200716110446496.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70)
