>在比赛做题过程中，感觉一些利用漏洞进行RCE的技巧非常巧妙，深入了解后发现都是利用了关于shell脚本的知识，感觉还是有必要系统学习一下shell语言的
### 简介
shell脚本最基础的用法是在linux系统里执行命令，不过在很多不同的编程语言中的命令执行都能见到shell有关的地方
"shell"指的是执行命令与操作系统交互的程序，而"bash"是最常用的linux/unix shell之一，因此shell和bash两个词一定程度上可以互换。
bash shell知识shell的一种类型，还有korn shell,C shell,Z shell等等其他shell，但是bash shell是最常见的
### 编写bash shell
shell命令提示符就像：`[username@host ~]$`，`$`后面就是要执行的命令，后面可以跟command [选项]  [参数]
另外$(command)在shell语法中能进行命令替换，具体如下：
- **先执行：** Shell 会先执行 `command` 这个命令（可以是任何 Shell 能执行的命令）。
- **捕获输出：** 捕获 `command` 命令在标准输出（stdout）上产生的文本。
- **替换文本：** 用捕获到的输出来**替换掉**整个 `$(command)` 结构。
- **形成最终命令：** 替换完成后，才将整个字符串作为最终要执行的命令。
*这里补充一点，在许多编程语言的命令行执行函数（最常见的是system)中都会启动一个shell解释器，然后将参数传到shell解释器里（一般是/bin/sh）。这时如果不能完全控制参数内容用$(command)来结合其他语法达成意想不到的操作*
### 创建和执行bash脚本
相比于命令行，bash脚本可以看作是多个命令行的集合，bash脚本也有一些语法规则：
##### 脚本文件的命名
bash脚本的后缀一般是.sh，不过即使没有.sh，bash脚本也能正常运行
##### bash脚本开头：shebang

shebang指的是一个由井号和叹号构成的字符序列`#!`。不同的shebang可以将后续的脚本内容按照不同的类Unix操作系统加载器shell调用程序来执行，Shebang 指向 bash 解释器的绝对路径。最常见的当然`!#/bin/bash`，不过也有其他的shebang：
- `#!/bin/sh`—使用sh，即Bourne shell或其它兼容shell执行脚本
- `#!/bin/csh`—使用csh，即C shell执行
- `#!/usr/bin/perl` -w—使用带警告的Perl执行
- `#!/usr/bin/python` -O—使用具有代码优化的Python执行
- `#!/usr/bin/php`—使用PHP的命令行解释器执行
可以使用`which bash`来找到shebang路径
以下是一个脚本的示例：
```
#!/bin/bash
echo "今天是 " `date`

echo -e "\n请输入目录路径"
read the_path

echo -e "\n 你的路径包含以下文件和文件夹："
ls $the_path
```
##### 执行bash脚本
执行前要先为用户分配权限
`chmod u+x run_all.sh`
这里，
- `chmod` 修改文件的所有权以供当前用户使用：`u`。
- `+x` 将执行权限添加到当前用户。这意味着作为所有者的用户现在可以运行该脚本。
- `run_all.sh` 是我们希望运行的文件。
您可以使用下列任何方法运行脚本：
- `sh run_all.sh`
- `bash run_all.sh`
- `./run_all.sh`
