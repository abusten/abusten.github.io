> _这道题做了快两天都没头绪，比赛结束看wp复现才发现原来还能这么做，遂写一篇笔记_
>

**一、题目描述**

打开题目容器，只显示“ Please go to /static/SCTF.jpg ”，没有其他任何提示。，访问/static/SCTF.jpg发现是一张图片。

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1727786673197-3fd72303-db74-420e-aaf3-d5c8dbc378ad.png)

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1727786993548-9ff475f3-86bf-4784-9d42-e001f37a6b24.png)

我做题时在这之后就访问了/robots.txt，还真让我搞到了后台管理系统的路径

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1727787222790-caa81163-4191-4619-a877-98e26f035c08.png)

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1727787253627-51dfd660-2c2b-400e-a814-bb064fbccc17.png)

之后还通过弱密码（admin和admin123456）搞到了管理员账号，结果到这就卡住了，虽然管理系统有文件上传的功能，但是无论上传什么文件都没法执行命令，·

