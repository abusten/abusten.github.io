> _最近做题发现之前以为是技巧的东西居然有个单独的知识点，挺基础的但是也容易忽略，还是总结一下吧_
>

**一、目录穿越**

**1.介绍**

 目录穿越（目录遍历）是一个Web安全漏洞，攻击者可以利用该漏洞读取运行应用程序的服务器上的任意文件。 这可能包括应用程序代码和数据，后端系统的登录信息以及敏感的操作系统文件。目录穿越不仅可以访问服务器中的任何目录，还可以访问服务器中任何文件的内容。例如，攻击者通过浏览器访问../../../../../../../../../../../../../../etc/passwd（此处较多../），就可以读取Linux服务器根目录下的etc目录下的passwd文件的内容。

  目录穿越比目录浏览、目录遍历更具破坏性，目录穿越不仅可以读取服务器中任何目录及任何文件的内容，还可以执行系统命令。又例如攻击者通过浏览器访问s/..%5c../Windows/system32/cmd.exe?/C+dir+C:，使用IIS中间件的s目录来变换目录并达到执行命令的目的。这个Web请求会返回C:所有文件列表，这是通过调用cmd.exe程序并执行dir C:命令来实现的。%5c是Web服务器的转换符，用来代表一些常见字符，这里表示的是反斜杠。

**2.原理**

1、./是当前目录

2、./是父级目录（回到当前文件夹下的，上一个文件夹）

3、/是根目录（回到最顶端的那个文件夹下）

**3.利用**

(1)当题目中遇到可以读取文件的功能时可以利用目录穿越读取服务器主机的文件内容

**例题：

moectf2024 垫刀之路04: 一个文件浏览器

打开后是一个文件系统

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1725610952094-b20b5730-a656-42bc-a09c-1f87701a45b2.png)

根目录有一个变量path可以读取文件系统里的文件内容

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1725611556663-7f3f92c1-829d-4a4b-a0c5-292f3555a48c.png)

利用目录穿越/?path=./src/../../../../../../../tmp/flag即可进入题目服务器的真文件系统，拿到flag

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1725614377839-19ca57be-8500-40f7-a28b-3cdf1e48c0bc.png)

(2)由于../表示上一级目录，因此./xxx/../../../../../../../../../../中xxx代表的目录不一定存在，可以绕过一些读取文件时的正则判断

**二、flag的常见位置**

> _做题时当找到能利用的漏洞后在拿到flag前经常会遇到通过读取题目文件拿到flag的步骤，但是找不到flag的位置却是一个经常遇到的问题，所以我决定写个笔记记录一下_
>

_	_web题中，flag的位置和出题人的习惯有关，大多数题目的flag文件都是直接放在根目录中，只要读取/flag就能直接获得flag，但当根目录中没有flag时，就需要一个寻找flag的简单流程了

1.在题目环境的配置文件中寻找，一般出题人会把flag配置在题目环境中，也就是/proc/self/environ,如果没有就翻/proc目录搜集信息，如果还没有看题目源码也可以看看index.php的源码内容寻找漏洞，还可以看看/proc/self/fd查看当前进程每个文件的提示符，还可以查看/proc/6/environ的内容然后从6往上叠加。

2.如果通过上面的方法找不到，还可以从/tmp目录下寻找flag，有些题目会把flag放在这个目录里。

3.以上方法都找不到的话，下面还有CTF题目中linux系统的常用文件，可以挨个试一试

**1. /etc目录**

(1) /etc目录下多是各种应用或系统配置文件，所以其下的文件是进行文件读取的首要目标。

(2)/etc/passwd

/etc/passwd文件是Linux系统保存用户信息及其工作目录的文件，权限是所有用户/组可读，一般被用作Linux系统下文件读取漏洞存在性判断的基准。读到这个文件我们就可以知道系统存在哪些用户、他们所属的组是什么、工作目录是什么。

(3) /etc/shadow

/etc/shadow是Linux系统保存用户信息及（可能存在）密码（hash）的文件，权限是root用户可读写、shadow组可读。所以一般情况下，这个文件是不可读的。

(4)/etc/apache2/*

/etc/apache2/*是Apache配置文件，可以获知Web目录、服务端口等信息。CTF有些题目需要参赛者确认Web路径。

(5)/etc/nginx*

/etc/nginx/是Nginx配置文件（Ubuntu等系统），可以获知Web目录、服务端口等信息。

(6)/etc/apparmor(.d)/*

是Apparmor配置文件，可以获知各应用系统调用的白名单、黑名单。例如，通过读配置文件查看MySQL是否禁止了系统调用，从而确定是否可以使用UDF（User Defined Functions）执行系统命令。

(7)/etc/(cron.d/*|crontab)

/etc/（cron.d/|crontab）是定时任务文件。有些CTF题目会设置一些定时任务，读取这些配置文件就可以发现隐藏的目录或其他文件。

(8)/etc/environment

/etc/environment是环境变量配置文件之一。环境变量可能存在大量目录信息的泄露，甚至可能出现secret_key泄露的情况。

(9)/etc/hostname

/etc/hostname表示主机名。不同的linux版本，这个配置文件也可能不同。比如Debian的对应文件是/etc/hostname

(10)/etc/hosts

/etc/hosts是主机名查询静态表，包含指定域名解析IP的成对信息。通过这个文件，参赛者可以探测网卡信息和内网IP/域名。

我们可以通过ssrf的file协议等来判断ip与对应的计算机。

一般情况下hosts文件的每行为一个主机，每行由三部份组成，每个部份由空格隔开。其中#号开头的行做说明，不被系统解释。

hosts文件的格式如下：

```plain
IP地址 主机名/域名 
第一部份：网络IP地址；
第二部份：主机名或域名；
第三部份：主机名别名；
```

(11)/etc/issue

/etc/issue指明系统版本。

(12)/etc/mysql/*

/etc/mysql/*是MySQL配置文件。

(13)/etc/php/*

/etc/php/*是PHP配置文件。

**2. /proc目录**

/proc目录通常存储着进程动态运行的各种信息，本质上是一种虚拟目录。注意：如果查看非当前进程的信息，pid是可以进行暴力破解的，如果要查看当前进程，只需/proc/self/代替/proc/[pid]/即可。

对应目录下的cmdline可读出比较敏感的信息，如使用mysql-uxxx-pxxxx登录MySQL，会在cmdline中显示明文密码：

```plain
/proc/[pid]/cmdline    ([pid]指向进程所对应的终端命令)

/proc/self/cmdline

```

有时我们无法获取当前应用所在的目录，通过cwd命令可以直接跳转到当前目录：

```plain
/proc/[pid]/cwd/     ([pid]指向进程的运行目录)

/proc/self/cwd

```

环境变量中可能存在secret_key，这时也可以通过environ进行读取：

```plain
/proc/[pid]/environ    ([pid]指向进程运行时的环境变量)
/proc/self/environ
```

指向启动当前进程的可执行文件（完整路径）的符号链接。通过exe文件我们可以获得指定进程的可执行文件的完整路径。[pid]指向进程所对应的可执行文件。有时我们想读取当前应用的可执行文件再进行分析，但在实际利用时可能存在一些安全措施阻止我们去读可执行文件，可以尝试访问：

```plain
/proc/self/exe
```

通过fd目录的文件获取进程，从而打开每个文件的路径以及文件内容

```plain
/proc/[pid]/fd/(1|2..)          (读取[pid]指向进程的stdout或stderror或其他)
/proc/[pid]/maps                ([pid]指向进程的内存映射)
/proc/[pid]/(mountslmountinfo)  ([pid]指向进程所在的文件系统挂载情况，CTF常见的是Docker环境，这时mount5会澄幕一些敏感路径)
/proc/[pid]/net/*               ([pid]指向进程的网络信息，如读取TCP将获取进程所绑定的TCP端口，ARP将泄露同网段内网IP信息)
```

```plain
/proc/self/fd
```

fd是一个目录，里面包含着当前进程打开的每一个文件的描述符（file descriptor）差不多就是路径啦，这些文件描述符是指向实际文件的一个符号连接，即每个通过这个进程打开的文件都会显示在这里。

查看指定进程打开的某个文件的内容。加上那个数字即可，在Linux系统中，如果一个程序用 open() 打开了一个文件，但是最终没有关闭它，即使从外部（如:os.remove(SECRET_FILE))删除这个文件之后，在/proc这个进程的 pid目录下的fd文件描述符目录下还是会有这个文件的文件描述符，通过这个文件描述符我们即可以得到被删除的文件的内容

其他目录

Nginx配置文件可能存在其他路径：

```plain
/usr/local/nginx/conf/*      (源代码安装或其他一些系统)
```

日志文件：

/var/log/* (经常出现Apache2的web应用可读/var/log/apache2/access.Log从而分析日志，盗取其他选手的解题步骤)

Apache默认Web根目录：

```plain
/var/www/html
```

在linux中，通过apache搭建一个网站，而该服务存在一些配置文件，用来对网站的根目录，日志设置等进行配置。在默认的情况下



1、采用RPM包安装：

默认情况下目录/usr 用来存放应用程序；/etc/apache

目录/etc 存放软件的配置文件：/etc/httpd/conf/httpd.conf



2、采用源代码安装：

默认在/usr/local下；/usr/local/apache

配置文件 /usr/local/apache/conf/httpd.conf



这是偶然看到的 没有验证 即说明apache的目录可能是apache apache2 需要视安装环境等而定。在 Ubnutu 上，apache 服务叫 apache2，而不是 httpd（在 Centos 上叫 httpd），主配置文件为 /etc/apache2/apache2.conf



下面的几个是关键的配置

/etc/httpd/是Apache服务器的根目录

/etc/httpd/conf/httpd.conf是Apache服务器的主配置文件，其中包含指定文档root的配置

/var/www/html/是Apache服务器的文档根目录 这也就是我们网站的常用的默认根目录

/etc/init.d/httpd是Apache服务器启动脚本文件

/var/log/httpd/access_log是Apache服务器的访问日志文件

/var/log/httpd/error_log是Apache服务器的错误日志文件



下面的是目录的组成 Bin目录中包括了

Apache服务器运行和管理所需的执行程序，其中httpd是服务器的执行程序，apachectl是服务器的启动脚本

Lib目录中保存了Apache服务器运行所需的库文件

Conf目录用于保存Apache服务器的配置文件，其中httpd.conf是Apache服务器的主配置文件 Htdocs目录是Apache服务器的文档根目录，该目录将作为Web服务器的根目录

Manual目录中保存了Apache服务器的帮助手册文件，文件是网页格式的，可以通过访问Apache服务器中的/manual目录阅读该目录下的帮助文件内容

Man目录用于保存Apache服务器手册页文件，文件被分别保存在man1和man8两个子目录中，可用man命令阅读指定的手册页文件查询目录的帮助信息

Logs目录是用于保存Apache服务器的日志文件

```plain
access_log文件是访问日志文件
error_log文件是错误日志文件
```

php.ini php配置文件

一般Apache安装php后，php配置文件默认加载位置在php/lib/文件夹下

可能的位置大概有：

如果采用RPM包安装，安装路径应在 /etc/ 目录下

PHP的配置文件：/etc/php.ini



如果采用源代码安装，一般默认安装在 /usr/local/lib 目录下

**PHP配置文件:**

```plain
/usr/local/lib/php.ini 
或/usr/local/php/lib/php.ini 
或 /usr/local/php/etc/php.ini  
或 /usr/local/apache2/conf/php.ini等
```

**PHP session目录：**

```plain
/var/lib/php(5)/sessions/    (泄露用户session)
```

<h3 id="812486f0"><font style="color:rgb(79, 79, 79);">用户目录：</font></h3>
```plain
[user_dir_you_know]/.bash_history         (泄露历史执行命今)
[user_dir_you_know]/.bashrc                   (部分环境变量)
[user_dir-you_know]/.ssh/id_rsa(.pub)     (ssh登录私钥/公钥)
[user_dir_you_know]/.viminfo                   (vim使用记录)
```

