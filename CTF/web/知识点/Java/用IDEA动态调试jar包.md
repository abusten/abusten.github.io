1. 首先新建一个项目，然后在项目的lib文件夹里放入jar包
2. 进入项目结构->库，添加目标jar包，之后就能看到jar包的被添加到依赖库中
![[Pasted image 20250821214253.png]]
3. 之后将运行模板设置为远程调试
![[Pasted image 20250821232028.png]]

注意：这里的5005是监听端口，不是访问端口，后面会具体介绍
![[屏幕截图 2025-08-21 232142.png]]
4. 之后在powershell里开启一个监听端口
```powershell
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 -jar D:\IdeaProjects\blade_cc\lib\app.jar
```
这里具体讲解一下这行命令
首先，调试不像运行一样可以直接java -jar app.jar，需要在开启一个JVM之后暂停运行，等一个调试器连接上来，显示运行时调用的各种函数，创建的各种类等内容，因此启动JVM之后需要和powershell连接一个socket
因此这行命令就是做如下工作：
- jdwp: Java Debug Wire Protocol，Java调试协议。
- transport=dt_socket: 使用标准的TCP套接字进行通信。
- server=y: 让这个JVM扮演**服务器**的角色，打开一个端口**监听**连接。
- suspend=y: 这是**最重要的参数**。它告诉JVM在启动后**立即暂停**，直到有调试器成功连接上来，它才会继续执行main方法。这样你就可以调试从程序启动第一行开始的所有代码。
- address=5005: 指定监听的端口号为 5005。
5. 启动远程调试
不过可能会出现一些问题，比如我遇到的：
```powershell
PS D:\IdeaProjects\blade_cc> java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 -jar D:\IdeaProjects\blade_cc\lib\app.jar
Listening for transport dt_socket at address: 5005
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : app.env          => default
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : app.pid          => 38836
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : app.devMode      => true
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : jdk.version      => 1.8.0_161
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : user.dir         => D:\IdeaProjects\blade_cc
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : java.io.tmpdir   => C:\Users\86150\AppData\Local\Temp\
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : user.timezone    => Asia/Shanghai
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : file.encoding    => GBK
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : app.classpath    => D:\IdeaProjects\blade_cc\lib\app.jar

                                         __, _,   _, __, __,
                                         |_) |   /_\ | \ |_
                                         |_) | , | | |_/ |
                                         ~   ~~~ ~ ~ ~   ~~~
                                     :: Blade :: (v2.1.1.RELEASE)

2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]          c.h.b.m.r.RouteMatcher : Add route  POST    /challenge
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]          c.h.b.m.r.RouteMatcher : Add route  GET     /
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : Register bean: [com.hellokaton.blade.Environment@67ac38ef, com.n1ght.controller.IndexController@663946ed]
2025/08/21 22:12:55  INFO [          _(:3」∠)_ ]             c.h.b.s.NettyServer : Use NioEventLoopGroup
2025/08/21 22:13:01 ERROR [          _(:3」∠)_ ]                     c.h.b.Blade : Bind address error
 java.net.BindException: Address already in use: bind
        at sun.nio.ch.Net.bind0(Native Method)
        at sun.nio.ch.Net.bind(Net.java:433)
        at sun.nio.ch.Net.bind(Net.java:425)
        at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:223)
        at io.netty.channel.socket.nio.NioServerSocketChannel.doBind(NioServerSocketChannel.java:141)
        at io.netty.channel.AbstractChannel$AbstractUnsafe.bind(AbstractChannel.java:562)
        at io.netty.channel.DefaultChannelPipeline$HeadContext.bind(DefaultChannelPipeline.java:1334)
        at io.netty.channel.AbstractChannelHandlerContext.invokeBind(AbstractChannelHandlerContext.java:506)
        at io.netty.channel.AbstractChannelHandlerContext.bind(AbstractChannelHandlerContext.java:491)
        at io.netty.channel.DefaultChannelPipeline.bind(DefaultChannelPipeline.java:973)
        at io.netty.channel.AbstractChannel.bind(AbstractChannel.java:260)
        at io.netty.bootstrap.AbstractBootstrap$2.run(AbstractBootstrap.java:356)
        at io.netty.util.concurrent.AbstractEventExecutor.safeExecute(AbstractEventExecutor.java:164)
        at io.netty.util.concurrent.SingleThreadEventExecutor.runAllTasks(SingleThreadEventExecutor.java:469)
        at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:503)
        at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:986)
        at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
        at java.lang.Thread.run(Thread.java:748)
```
这个问题就是Java web框架的应用程序试图运行结果端口被占用了，于是我试图关闭占用我运行的进程
```powershell
PS D:\IdeaProjects\blade_cc> netstat -ano | findstr :9000
  TCP    0.0.0.0:9000           0.0.0.0:0              LISTENING       31968
  TCP    [::]:9000              [::]:0                 LISTENING       31968
PS D:\IdeaProjects\blade_cc> tasklist | findstr "31968"
idea64.exe                   31968 Console                    1  2,144,672 K
```
结果发现占用进程的就是idea，没办法关闭，不过可以改变web框架运行的端口，命令如下：
```powershell
 java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 -jar D:\IdeaProjects\blade_cc\lib\app.jar --server.port=9001
```
加了一个`--server.port=9001`，大多数java框架都支持，之后就可以运行了
