> _反射是框架设计的灵魂。_

**框架：半成品软件，可以在框架的基础上进行软件开发，简化代码编写量。**

**反射：将类的各个组成部分封装为其他对象，这就是反射机制。**

众所周知，java需要先编译在运行，java文件从被javac编译为.class文件阶段到Runtime运行阶段这之间需要类加载器ClassLoader给Java类初始化，而这就构成了java从编译到运行的三个阶段。

1.source源代码阶段：

这个阶段包括从开始编写java代码到运行编译后的.class文件之前，包括保存java文件和javac命令编译成.class文件。这个阶段所有的文件都保存在硬盘里，而代码的执行需要cpu，但cpu只能读取内存里的数据，所以还需要将数据从硬盘传输到内存这个步骤。

2.Runtime执行阶段

这个阶段里java类的对象都存在内存里运行，这就说明肯定由于一个阶段是将数据从硬盘转移到内存。

3.class类对象阶段

这个阶段就是java程序从硬盘加载到内存的第二阶段。class文件是通过类加载器加载进内存的，对应的是java里的一个对象ClassLoader。这个阶段里有一个class类对象描述class字节码文件（java里存在class类来描述字节码文件里所有的共同特征和行为），class类对象中有成员变量Feild[] feild对象，构造方法Constructor[] cons对象和成员方法Method[] method对象，他们的功能分别是给class字节码文件里类的属性变量，构造方法和成员对象，这个阶段可以通过上面class类对象里的行为创建Runtime执行阶段里真正的对象，所以这个过程就是上面提到的反射机制。

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1742275613201-58b6053c-f2a1-47a4-a6c1-6214d4724557.png)

**JVM框架图**：

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1742275687459-2014c9ae-a748-43b4-8e00-7f9a35b6ab49.png)

JVM会先解析class文件的内容再执行java文件，class就是javac命令生成的字节码。

类加载器中最顶层的是Bootstrap ClassLoader（引导类加载器）Extension ClassLoader（扩展类加载器）App ClassLoader（系统类加载器）是默认的类加载器，如果类加载时我们不指定类加载器的情况下，默认会使用AppClassLoade加载类，ClassLoader.getSystemClassLoader()返回的系统类加载器也是AppClassLoader。

<font style="color:rgb(51, 51, 51);">类有如下核心方法：</font>

1. `loadClass`（加载指定的Java类）
2. `findClass`（查找指定的Java类）
3. `findLoadedClass`（查找JVM已经加载过的类）
4. `defineClass`（定义一个Java类）
5. `resolveClass`（链接指定的Java类）

**类加载隔离**

<font style="color:rgb(51, 51, 51);">创建类加载器的时候可以指定该类加载的父类加载器，ClassLoader是有隔离机制的，不同的ClassLoader可以加载相同的Class（两者必须是非继承关系），同级ClassLoader跨类加载器调用方法时必须使用反射。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1742301967173-afdaaa18-3a87-45dc-8c44-a364e5527e0b.png)
**反射的作用**：让java具有动态性，可以让jav在运行时动态创建对象
