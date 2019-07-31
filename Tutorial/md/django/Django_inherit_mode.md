Django模型继承方式：

- 抽象基类

  父类不会被创建数据表， 子类默认继承父类Meta， 但abstract默认被设置成False

- 多表继承

  - 父类会被创建成数据表， 子类不继承父类的Meta除ordering、get_latest_by属性。若不想继承可设置：ordering=[]

  ```python
  class Sample(Father):
      ...
      class Meta:
          db_table = 'sample'
          ordering = []
  ```

  - 会自动创建连接至父类的OneToOneField:

    ```python
    sample_str = models.OneToOneField(Father, on_delete=models.CASCADE, parent_link=True)
    ```

    

- 代理模型



#### Mysql

##### modify database character

alter database name default character set utf8;

##### modify table character

alter table name default character set utf8

##### modify column character

alter table name change column_name varchar(100) character set utf8

##### modify table & column

alter table name convert to character set utf8



​	**export**

​	mysqldump -u root -p database tablename > target.sql ;

​	

​	**import**

​	source target.sql



