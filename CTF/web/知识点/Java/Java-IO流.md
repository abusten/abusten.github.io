  作为攻击者，最终的目的是命令执行，所以这篇文章主要探讨最终目的是如何在java环境里执行命令。
## 前言

IO是指 Input/Output，即输入和输出。以内存为中心：

为什么要把数据读到内存才能处理这些数据？因为代码是在内存中运行的，数据也必须读到内存，最终的表示方式无非是 byte数 组，字符串等，都必须存放在内存里。

从 Java 代码来看，输入实际上就是从外部，例如，硬盘上的某个文件，把内容读到内存，并且以 Java 提供的某种数据类型表示，例如，`byte[]`，`String`，这样，后续代码才能处理这些数据。

因为内存有“易失性”的特点，所以必须把处理后的数据以某种方式输出，例如，写入到文件。Output 实际上就是把 Java 表示的数据格式，例如，`byte[]`，`String`等输出到某个地方。

IO 流是一种顺序读写数据的模式，它的特点是单向流动。数据类似自来水一样在水管中流动，所以我们把它称为 IO 流。

在讲 IO 流之前，我们先讲一讲 Java 关于文件的一些操作。
## 创建文件的三种方式

因为与文件有关，我这里的路径也贴出来比较好

> `Reappearance\Serialable\src\IOStream`
> 
> 准备将文件都放到新建的 `CreateForFile` 文件夹中

建议路径跑通一个之后，其余复制粘贴路径。

### 1. 根据路径创建一个 File 对象

- 方法 `new File(String pathname)`

```java
package src.IOStream;    
    
import java.io.File;    
import java.io.IOException;    
    
// 根据路径创建一个 File 对象    
public class newFile {    
    public static void main(String[] args) {    
        createFile();    
 }    
    public static void createFile(){    
        File file = new File("Serialable/src/IOStream/CreateForFile/new1.txt");    
 try{    
            file.createNewFile();    
 System.out.println("Create Successfully");    
 } catch (IOException e){    
            e.printStackTrace();    
 }    
    }    
    
}
```
### 2. 根据父目录 File 对象，在子路径创建一个文件

- 方法 `new File(File parent, String child)`
```java
package src.IOStream;    
    
import java.io.File;    
import java.io.IOException;    
    
// 根据父目录File对象，在子路径创建一个文件    
public class newFile02 {    
    public static void main(String[] args) {    
        createFile();    
	 }    
    public static void createFile(){    
        File parentFile = new File("Serialable/src/IOStream/CreateForFile");    
	 File file = new File(parentFile, "new2.txt");    
	 try{    
            file.createNewFile();    
			 System.out.println("Create Successfully");    
	 } catch (IOException e){    
            e.printStackTrace();    
		}    
	}    
}
```

其实和第一个方法大同小异。

### 3. 根据父目录路径，在子路径下生成文件

- 方法 `new File(String parent, String child)`

和之前两种方法还是有一些差距的。
```java
package src.IOStream;    
    
import java.io.File;    
import java.io.IOException;    
    
// 根据父目录路径，在子路径下生成文件    
public class newFile03 {    
    public static void main(String[] args) {    
        createFile();    
 }    
    public static void createFile(){    
        String parentPath = "Serialable/src/IOStream/CreateForFile";    
 String fileName = "new3.txt";    
 File file = new File(parentPath, fileName);    
 try{    
            file.createNewFile();    
 System.out.println("Create Successfully");    
 } catch (IOException e){    
            e.printStackTrace();    
 }    
    }    
}
```
创建三个 txt 文件。
## 0x03 获取文件信息

我们先在 new1.txt 当中编辑一些消息

![[FileContents 1.png]]

我们通过 `file` 类的方法名进行一些基本信息的获取
```java
package src.IOStream;    
    
import java.io.File;    
    
public class GetFileInfo {    
    public static void main(String[] args) {    
        getFileContents();    
 }    
    
    public static void getFileContents(){    
        File file = new File("Serialable/src/IOStream/CreateForFile/new1.txt");    
 System.out.println("文件名称为：" + file.getName());    
 System.out.println("文件的绝对路径为：" + file.getAbsolutePath());    
 System.out.println("文件的父级目录为：" + file.getParent());    
 System.out.println("文件的大小(字节)为：" + file.length());    
 System.out.println("这是不是一个文件：" + file.isFile());    
 System.out.println("这是不是一个目录：" + file.isDirectory());    
 }    
}
```

输出如图
![[GetContensOut.png]]
## 目录与文件操作

### 1. 文件删除

- 使用 `file.delete(文件)`
```java
package src.IOStream;    
    
import java.io.File;    
import java.lang.reflect.Field;    
    
// 文件删除    
public class FileDelete {    
    public static void main(String[] args) {    
        deleteFile();    
 }    
    public static void deleteFile(){    
        File file = new File("Serialable/src/IOStream/CreateForFile/new1.txt");    
 System.out.println(file.delete() ? "Delete Successfully":"Delete failed");    
 }    
}
```

### 2.目录删除

- 方法 `file.delete(目录)`，这里有个小坑，只有空的目录才可以删除，不然会显示删除失败。
- 我在 `CreateForFile` 同级目录下新建了一个文件夹 `CreateForDelete` 用以测试。
```java
package src.IOStream;    
    
import java.io.File;    
    
//删除目录    
public class DirectoryDelete {    
    public static void main(String[] args) {    
        deleteDirectory();    
 }    
    public static void deleteDirectory(){    
        File file = new File("Serialable/src/IOStream/CreateForDelete");    
 System.out.println(file.delete()? "Delete Successfully":"Delete failed");    
 }    
}
```

### 3. 创建单级目录

- 方法 `file.mkdir()`
```java
package src.IOStream;    
    
import java.io.File;    
    
// 创建单级目录    
public class CreateSingleDirectory {    
    public static void main(String[] args) {    
        createSingleDir();    
 }    
    public static void createSingleDir(){    
        File file = new File("Serialable/src/IOStream/CreateForDirectory");    
 System.out.println(file.mkdir() ? "Create Successfully":"Create failed");    
 }    
}
```

成功创建

### 4. 创建多级目录

- 方法 `file.mkdirs()`，注意多了个 **s** 别搞错了。

```java
package src.IOStream;    
    
import java.io.File;    
    
// 创建多级目录    
public class CreateMultiDirectory {    
    public static void main(String[] args) {    
        createMultiDir();    
 }    
    
    public static void createMultiDir(){    
        File file = new File("Serialable/src/IOStream/CreateMultiDirectory/test");    
 System.out.println(file.mkdirs() ? "Create Successfully":"Create failed");    
    
 }    
}
```
## 回归 IO 知识点 —— IO 流分类

按照操作数据单位不同分为：**字节流**和**字符流**

- 字节流（8bit，适用于二进制文件）
- 字符流（按字符，因编码不同而异，适用于文本文件）

按照数据流流向不同分为：**输入流**和**输出流**
按照流的角色不同分为：**节点流**，**处理流/包装流**

|抽象基类|字节流|字符流|
|---|---|---|
|输入流|InputStream|Reader|
|输出流|OutputStream|Writer|

- 到这里就非常重要了，因为它与我们后续的命令执行直接相关。这些 IO 流在我们命令执行的 Payload 当中充当着缓冲的作用。