>理论题基本上就不记录了
# Meow
nmap信息搜集：`nmap -sV {PORT}`
nmap使用方法：
```
端口扫描：nmap {IP}（默认扫描1000个端口）
指定端口：-p
nmap IP -p 80
nmap IP -p 1-80
nmap IP -p 80,3389,22,21
nmap IP -p 1-65535
nmap IP -p-    # -p- 等价于 -p 1-65535
TCP全连接扫描：nmap IP -p 80 -sT
检测是否进行完整的三次握手
SYN半链接扫描：nmap IP -p 80 -sV
检测是否进行两次握手
服务识别：nmap IP -sV
不但检测端口的服务，还检测服务版本
提高扫描速度（会降低扫描精确性）：--min-rate 5000#指每秒至少发送5000个数据包
-T<0-5>#数字越大扫描速度越快
```
telnet协议：
远程连接，采用的是TCP/IP协议。端口23，因为明文传输所以不如ssh安全
`telnet IP`连接之后root/root登录即可获取flag
# Fawn
_FTP 代表File Transfer Protocol 文件传输协议_。这是一种网络/通信协议，用于通过TCP/IP（传输控制协议/Internet 协议）网络在计算机之间传输文件，默认端口22。FTP也由于明文传输的原因不安全，不过有类似于ssh一样密文传输的版本SFTP。
`ftp IP`之后用户名`anonymous`登录`get flag.txt`即可下载flag
# Dancing
SMB(全称是Server Message Block)是一个协议名，可用于在计算机间共享文件、打印机、串口等，电脑上的网上邻居就是靠它实现的。端口号445。

SMB 是一种客户机/服务器、请求/响应协议。通过 SMB 协议，客户端应用程序可以在各种网络环境下读、写服务器上的文件，以及对服务器程序提出服务请求。此外通过 SMB 协议，应用程序可以访问远程服务器端的文件、以及打印机等资源。

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-11 18:55 CST
Nmap scan report for 10.129.1.12
Host is up (0.30s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```
其中`microsoft-ds`就是SMB服务名称
`smbclient -L //IP/`可以显示所有的SMB服务共享
之后`smbclient //10.129.1.12/WorkShares`连接get拿flag
# 