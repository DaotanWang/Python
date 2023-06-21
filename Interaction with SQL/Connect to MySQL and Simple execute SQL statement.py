import pymysql

db = pymysql.connect(host='10.20.30.40',
                     user='username',
                     password='password',
                     database='xxx_database')#库名
cursor = db.cursor()#python无法直接执行SQL语句，使用cursor帮助执行语句。

#SELECT
sql = """select * from table_name WHERE domain_type="xxx" AND country_code="xxx" AND product_category IS NULL;"""
cursor.execute(sql)#执行
data = cursor.fetchall()#返回满足条件的所有行，以多个元组为元素的列表返回。
print(data)# [(1,2,3), (4,5,6), ...]
print(data[0][1])# 2


#单条记录更新/插入用execute简单直接
#UPDATE
domain = "ABC.com"
cursor.execute(
                """
                    UPDATE table_name AS tt
                    SET tt.domain_ascore='xxx',tt.monthly_organic_traffic='xxx'
                    WHERE tt.country_code='xxx' AND tt.product_category='xxx' AND tt.domain='%s';
                """%domain
                )
db.commit()#提交事务，修改数据库才需要，SELECT只读取，所以不用。

#INSERT
#假如有三个字段name,email,address
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s);", ('James', 'james@example.com'))
#只在name,email这里新增一条值，其他字段默认为空,如果不指定name、email，Value会按顺序注入表中%s数量一定要和实际的字段数量相同，不然会报错。
cursor.execute("INSERT INTO users VALUES (%s, %s,%s);", ('James', 'james@example.com',''))
db.commit()


#批量记录更新/插入用executemany
#UPDATE
data = [
    ("Jim", "James"),   # 更新第一条记录
    ("John", "John"),   # 保持第二条记录不变
    ("Jane", "Jane")    # 保持第三条记录不变
]
cursor.executemany("UPDATE users SET name=%s WHERE name=%s;", data)#一组一组按顺序带进去执行
db.commit() 

#INSERT
data = [
    ('James', 'james@example.com'),
    ('John', 'john@example.com'),
    ('Jane', 'jane@example.com') 
]
cursor.executemany("INSERT INTO users (name, email) VALUES (%s, %s);", data)
db.commit()

#DELECT一样的，也可以用这两个方法执行
cursor.execute("DELETE FROM users WHERE name = 'James';")

names_to_delete = ['John', 'Jane', 'Bob']
cursor.executemany("DELETE FROM users WHERE name = %s;", names_to_delete) 
db.commit()



