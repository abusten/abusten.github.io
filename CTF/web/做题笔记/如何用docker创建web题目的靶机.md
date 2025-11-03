> 在本地测试和部署web题目靶机时每做一遍都要从网上搜一遍，所以还是写一个笔记记录一下过程吧
>

**一.docker命令总结**

```bash
docker pull ubuntu:16.04                # 拉取对应镜像

docker images		                # 查看当前系统中存在镜像 

docker ps          	                # 查看运行中的容器
docker ps -a       	                # 查看所有容器（包括已结束运行的）

docker cp 主机文件名 容器id:容器指定目录  # 将主机文件复制到指定位置，反之则交换位置
```

```bash
docker run -it 容器id		      # 以交互模式运行容器，为容器重新分配一个伪输入终端
docker run -d 容器id		      # 后台运行容器，并返回容器ID
```

```bash
docker stop 容器id 	            #停止指定容器
docker stop $(docker ps -a -q)      #停止所有已经运行的容器

docker rm 容器id   	            #删除指定容器，删除前先停止
docker rm $(docker ps -a -q)        #删除所有已经停止的指令

docker rmi 镜像id		    # 删除指定镜像
```

```bash
docker exec -it 容器id  /bin/bash  	# 进入容器的bash界面
docker attach 容器id			# 进入容器内部
exit                                    # 进入docker内部后退出容器
```

```bash
docker port 容器id   				# 查看容器映射端口
netstat -tlnp					# 查看主机开放端口
systemctl status firewalld			# 查看防火墙状态
systemctl stop firewalld			# 暂时关闭防火墙
```

```bash
docker export 容器id > ctf.tar			# 导出为tar文件
docker save 镜像name  > ./ctf.tar		# 将→指定镜像名←保存成 tar 归档文件
cat ctf.tar | docker import - ctf               # 可以这样导入
```

```bash
docker build -t 镜像name -f dockerfile文件名
```

**二.具体步骤**

> _(由于我的电脑c盘空间不够用了，在wsl里搞这些有点占空间，所以以下步骤我都是在虚拟机里做的）_

部署题目时大多是有个Dockerfile文件的，先在Dockerfile所在文件夹里打开控制台，首先进root，然后docker build拉镜像，这一步如果之前没下载过类似于php或nginx的镜像但是运行需要（具体得看dockerfile怎么写的）的话还要联外网下载，不然这一步会失败，如果失败的话主机代理记得开Tun，之后如果想检查拉镜像是否成功可以docker images看看

下一步是开启容器，用docker run，一般需要-p选择一个空的端口，docker ps可以检查容器是否开启成功，如果成功运行那么现在就能从虚拟机的localhost:端口访问了

如果想从主机访问题目需要ifconfig -a一下来查看虚拟机的地址

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1737637127122-d469fd37-2b43-4437-8591-f41348781257.png)

像这样选中的地方就是虚拟机的地址了，只要在主机的浏览器里访问61.139.2.128:题目端口就能成功访问题目容器了

