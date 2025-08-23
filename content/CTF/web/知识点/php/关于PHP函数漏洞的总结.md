**一.preg_replace**

```php
mixed preg_replace ( mixed $pattern , mixed $replacement , mixed $subject [, int $limit = -1 [, int &$count ]] )
```

	

| **<font style="color:rgb(169, 190, 207);">参数</font>** | **<font style="color:rgb(169, 190, 207);">说明</font>** |
| :--- | :--- |
| <font style="color:rgb(169, 190, 207);">$pattern</font> | <font style="color:rgb(169, 190, 207);">要搜索的模式，可以是字符串或一个字符串数组</font> |
| <font style="color:rgb(169, 190, 207);">$replacement</font> | <font style="color:rgb(169, 190, 207);">用于替换的字符串或字符串数组</font> |
| <font style="color:rgb(169, 190, 207);">$subject: 要搜索替换的目标字符串或字符串数组</font> | |
| <font style="color:rgb(169, 190, 207);">$limit</font> | <font style="color:rgb(169, 190, 207);">可选，对于每个模式用于每个 subject 字符串的最大可替换次数。默认是 -1（无限制）</font> |
| <font style="color:rgb(169, 190, 207);">$count</font> | <font style="color:rgb(169, 190, 207);">可选，为替换执行的次数</font> |
| <font style="color:rgb(169, 190, 207);">如果 subject 是一个数组， preg_replace() 返回一个数组，其他情况下返回一个字符串。如果匹配被查找到，替换后的 subject 被返回，其他情况下 返回没有改变的 subject。如果发生错误，返回 NULL。</font> | |
| <font style="color:rgb(169, 190, 207);">这个函数有个 “/e” 漏洞，“/e” 修正符使 preg_replace() 将 replacement 参数当作 PHP 代码进行执行。如果这么做要确保 replacement 构成一个合法的 PHP 代码字符串，否则 PHP 会在报告在包含 preg_replace() 的行中出现语法解析错误。</font> | |


  
 例题：

```php
    $pattern = $_GET[pat];
    $replacement = $_GET[rep];
    $subject = $_GET[sub];

    if (isset($pattern) && isset($replacement) && isset($subject)) {
        preg_replace($pattern, $replacement, $subject);
    }else{
        die();
    }
```

只要在sub中匹配pat的内容，并在rep前加上/e修正符，就能执行rep参数赋值的php代码，例如

`<font style="color:rgb(179, 103, 103);">?pat=/abc/e&rep=</font><font style="color:rgb(227, 95, 156);">system(</font><font style="color:rgb(255, 122, 48);">'ls')&</font><font style="color:rgb(227, 95, 156);">sub</font><font style="color:rgb(200, 195, 188);">=</font><font style="color:rgb(134, 109, 172);">abc</font>`

就能成功执行system('ls')。

**二.assert()**

`assert(mixed $assertion, Throwable|string|null $description = null): bool`

assert() 会检查指定的 assertion 并在结果为 FALSE 时采取适当的行动

assert()函数其实是一个断言函数。

这个函数在php语言中是用来判断一个表达式是否成立。返回true or false;

如果 assertion 是字符串，它将会被 assert() 当做 PHP 代码来执行。

（例题详见我的做题笔记：攻防世界 mfw)

**三.in_array()**

`in_array(mixed $needle, array $haystack, bool $strict = false): bool`

大海捞针，在大海（haystack）中搜索针（ needle），如果没有设置 strict 则使用宽松的比较。

这个函数的漏洞是当$strict设置为false（严格模式关闭）时，会对$haystack和$needle中的元素进行弱比较

（例如$needle=7shell.php会强制转换为$needle=7再进行比较)

**四.is_numeric()**

`bool is_numeric ( mixed $var )`

is_numeric() 函数用于检测变量是否为数字或数字字符串。PHP 版本要求：PHP 4, PHP 5, PHP 7

is_numeric函数对于空字符%00，无论是%00放在前后都可以判断为非数值，而%20空格字符只能放在数值后。

