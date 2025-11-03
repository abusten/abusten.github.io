以下内容均在已经给操作系统下载golang编译器和环境变量之后完成
# 创建项目并运行
新建go项目，配置项目地址，配置代理为`GOPROXY=https://goproxy.cn`，通过中间代理商来为用户提供包下载
首先，应该项目的目录结构里一般有以下部分：
- `bin`文件目录：用于存放编译生成的可执行文件`.exe`
- `src`文件目录：用于存放源代码
- `pkg`文件目录：存放依赖包
- `go.mod`包管理文件就放在`src`下面就行。
在设置中添加一个project Gopath并设置成项目里的src目录存放源码，取消勾选使用系统环境中的gopath
![[Pasted image 20251030152918.png]]
也可以在下面的go module里配置go的包代理下载地址
# 配置运行方式
一个简单的项目目录结构：
![[Pasted image 20251030153622.png]]
GoLand 中，运行 Go 有三种方式：
- 文件方式运行（File）
- 以包的方式运行（Package）
- 以整个目录的方式运行（Directory）
# 以文件方式运行
以文件方式运行最简单，只需要右键文件Run就行，编译生成的可执行文件位于用户目录`C:\Users\username\AppData\Local\Temp\GoLand\`下，并不在`bin`文件中。
