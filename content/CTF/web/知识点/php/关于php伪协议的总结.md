**一.php://**

用于访问各个输入/输出流(I/O stream)。一般常用php://filter或php://input。php://filter用于读取文件内容，php://input用于执行代码。

1.php://filter

该协议会的参数会在该协议路径上传递，多个参数可以在同一个路径里传递，具体如下：

| **<font style="color:rgb(209, 205, 199);">php://filter 参数</font>** | **<font style="color:rgb(209, 205, 199);">描述</font>** | |
| :--- | :--- | --- |
| <font style="color:rgb(209, 205, 199);">resource=<要过滤的数据流></font> | <font style="color:rgb(209, 205, 199);">必须项。它指定了你要筛选过滤的数据流。</font> | |
| <font style="color:rgb(209, 205, 199);">read=<读链的过滤器></font> | <font style="color:rgb(209, 205, 199);">可选项。可以设定一个或多个过滤器名称，以管道符（*\</font> | <font style="color:rgb(209, 205, 199);">*）分隔。</font> |
| <font style="color:rgb(209, 205, 199);">write=<写链的过滤器></font> | <font style="color:rgb(209, 205, 199);">可选项。可以设定一个或多个过滤器名称，以管道符（\</font> | <font style="color:rgb(209, 205, 199);">）分隔。</font> |
| <font style="color:rgb(209, 205, 199);"><; 两个链的过滤器></font> | <font style="color:rgb(209, 205, 199);">任何没有以</font><font style="color:rgb(209, 205, 199);"> </font>_<font style="color:rgb(209, 205, 199);">read=</font>_<font style="color:rgb(209, 205, 199);"> </font><font style="color:rgb(209, 205, 199);">或</font><font style="color:rgb(209, 205, 199);"> </font>_<font style="color:rgb(209, 205, 199);">write=</font>_<font style="color:rgb(209, 205, 199);"> </font><font style="color:rgb(209, 205, 199);">作前缀的筛选器列表会视情况应用于读或写链。</font> | |


 		使用实例：

`php://filter/read=convert.base64-encode/resource=[目标文件]`

**二.file://**

用于以本地文件系统的形式访问文件，而不是以网页url的形式访问

