# 为什么写的项目总是无法运行
就算是最简单的一个go项目`main.go`,在写完保存之后想运行，除了编译为二进制文件运行以外，如果想以文件方式运行的话（比如vscode直接右键run code），如果是项目只有一个源代码文件也没调用第三方包会正常运行，因为自动套用了GOPATH模式，将一个目录里的代码都当做根目录再自动解析文件；可如果写项目时使用了跨包调用，或者使用了第三方包，就需要用一个go.mod（最好调用第三方包时先`go mod init <module name>`一下，再go get和go mod tidy）

# go.mod有什么用
go.mod是Go module声明文件，可以理解为依赖清单+模块身份
常见的go.mod:
```go.mod
module example.com/myproject

go 1.22

require (
    github.com/PuerkitoBio/goquery v1.8.1
)
```
- - `module`：给你的项目一个全局唯一的路径（本地练习也可以用短名字，比如 `module scrape`）。
    - go：声明使用的 Go 版本，编译器会按此设置语义差异。
    - `require`/`replace`/`exclude`：依赖管理相关。
- 常用命令：
    
    - `go mod init <module>`：在当前目录生成新的 `go.mod`。
    - `go mod tidy`：自动分析源码，补齐缺失依赖并清理未使用的条目。
    - `go list -m all`：查看当前模块依赖树。
    - `go env GOPATH` / `GO111MODULE`：检查环境配置。
- **有 `go.mod` 并不代表一定能运行**。还需要：正确的源码结构、可解析的导入路径、主函数存在、必要依赖能下载成功等。
