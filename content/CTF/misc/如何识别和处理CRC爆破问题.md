**一.CRC码的原理**

循环冗余校验码简称CRC码,是目前使用非常广泛的数据校验方式.它不仅能校验传递过来的数据正确性,还能筛查出哪一位出现了错误.它的局限性是只能校验一位数据发生跳变,在现实世界当中数据发生跳变很大很大的概率只有一位发生变化,因此CRC码也拥有很大的发挥舞台.

以下是crc码的编码方式：

1.将待编码的k位有效数据M(x)左移r位，得到全编码多项式M(x)*xr,空出r位，以装填r位余数

2.选取一个r+1位的生成多项式G(x)，对M(x)*xr进行模2除运算，得到商Q(x)和余数R(x)的代码

3.将左移r位的待编码信息，与余数R(x)模2加，可拼接为包含有效数据在内的CRC编码

举个例子：

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1737458082384-4cdbf925-dad7-49bf-88e0-95e47713c52c.png)

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1737458096442-39303855-6b2b-4327-92ae-198c60f4065f.png)

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1737458119261-65364270-c37b-4b9e-aceb-f2671f8994e7.png)<font style="color:rgb(34, 34, 34);">不同的标准采用的Q</font><sub><font style="color:rgb(34, 34, 34);">(x)</font></sub><font style="color:rgb(34, 34, 34);">不同  
</font><font style="color:rgb(34, 34, 34);">CRC4：x</font><sup><font style="color:rgb(34, 34, 34);">4</font></sup><font style="color:rgb(34, 34, 34);">+x+1  
</font><font style="color:rgb(34, 34, 34);">CRC8: x</font><sup><font style="color:rgb(34, 34, 34);">8</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">5</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">4</font></sup><font style="color:rgb(34, 34, 34);">+1  
</font><font style="color:rgb(34, 34, 34);">CRC16: x</font><sup><font style="color:rgb(34, 34, 34);">16</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">12</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">5</font></sup><font style="color:rgb(34, 34, 34);">+1  
</font><font style="color:rgb(34, 34, 34);">CRC32: x</font><sup><font style="color:rgb(34, 34, 34);">32</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">26</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">23</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">22</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">16</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">12</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">11</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">10</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">8</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">7</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">5</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">4</font></sup><font style="color:rgb(34, 34, 34);">+x</font><sup><font style="color:rgb(34, 34, 34);">2</font></sup><font style="color:rgb(34, 34, 34);">+x+1</font>

**二.CRC爆破在CTF中的应用**

大多数需要用到CRC码的题目都是CRC32码，做常见的用法是根据png的crc码判断出图片的真实宽高，下面是一个例子：

![](https://cdn.nlark.com/yuque/0/2025/jpeg/43146588/1737459319171-6b60ed51-d8bb-4cf7-a634-71ddae16907b.jpeg)

将上述图片YVL.jpg用foremost分离文件得到一张纯黑png图片00000149.png

将图片放进010里发现

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1737461046117-a6971d17-031f-4c94-afe0-04d3ed88f7e4.png)

下面提示crc不匹配

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1737461248000-c8e49b5d-5e06-4668-bab6-be3b7ec7de5f.png)

以上png文件格式为：

89 50 4E 47 0D 0A 1A 0A为png文件头

00 00 00 0D为数据块长度

49 48 44 52为文件头数据块标示IDCH

00 00 01 68:宽度

00 00 01 C2:高度

08 00 00 00 00:每一位依次表示 图像深度， 颜色类型， 压缩方法， 滤波器方法，隔行扫描方法

EF 1B 39 BE:CRC32校验码

crc码爆破，脚本如下：

```python
import binascii
import struct
 
 
 
crcbp = open("图片路径", "rb").read()    #打开图片
crc32frombp = int(crcbp[29:33].hex(),16)     #读取图片中的CRC校验值
print(crc32frombp)
 
for i in range(4000):                        #宽度1-4000进行枚举
    for j in range(4000):                    #高度1-4000进行枚举
        data = crcbp[12:16] + \
            struct.pack('>i', i)+struct.pack('>i', j)+crcbp[24:29]
        crc32 = binascii.crc32(data) & 0xffffffff
        #print(crc32)
        if(crc32 == crc32frombp):            #计算当图片大小为i:j时的CRC校验值，与图片中的CRC比较，当相同，则图片大小已经确定
            print(i, j)
            print('hex:', hex(i), hex(j))
            exit(0)
```

  
 

