原理：[https://www.synacktiv.com/publications/php-filter-chains-file-read-from-error-based-oracle#affected-functions](https://www.synacktiv.com/publications/php-filter-chains-file-read-from-error-based-oracle#affected-functions)

受影响的函数：

| **<font style="color:rgb(34, 34, 34);">Function</font>** | **<font style="color:rgb(34, 34, 34);">Pattern</font>** |
| --- | --- |
| _**<font style="color:rgb(34, 34, 34);">file_get_contents</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">file_get_contents($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">readfile</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">readfile($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">finfo->file</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = new finfo(); $fileinfo = $file->file($_POST[0], FILEINFO_MIME);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">getimagesize</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">getimagesize($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">md5_file</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">md5_file($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">sha1_file</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">sha1_file($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">hash_file</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">hash_file('md5', $_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">file</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">file($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">parse_ini_file</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">parse_ini_file($_POST[0]);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">copy</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">copy($_POST[0], '/tmp/test');</font>**` |
| _**<font style="color:rgb(34, 34, 34);">file_put_contents (only target read only with this)</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">file_put_contents($_POST[0], "");</font>**` |
| _**<font style="color:rgb(34, 34, 34);">stream_get_contents</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "r"); stream_get_contents($file);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">fgets</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "r"); fgets($file);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">fread</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "r"); fread($file, 10000);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">fgetc</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "r"); fgetc($file);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">fgetcsv</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "r"); fgetcsv($file, 1000, ",");</font>**` |
| _**<font style="color:rgb(34, 34, 34);">fpassthru</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "r"); fpassthru($file);</font>**` |
| _**<font style="color:rgb(34, 34, 34);">fputs</font>**_ | `**<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">$file = fopen($_POST[0], "rw"); fputs($file, 0);</font>**` |


利用工具：[https://github.com/synacktiv/php_filter_chains_oracle_exploit](https://github.com/synacktiv/php_filter_chains_oracle_exploit)

我已经下载在电脑里了，在[这里]("D:\86150\CTF题目\tools\php_filter_chains_oracle_exploit-main")

注：侧信道攻击本质上是靠猜的，所以并不能读取到全部文件内容，并且每次使用工具读取的内容都不一样，所以要多试几次

