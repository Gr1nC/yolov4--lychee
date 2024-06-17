import sqlite3

# 创建一个访问SQLite数据库的连接，当指定的数据库文件不存在，会自动创建
conn = sqlite3.connect('info.sqlite')
# 创建游标对象cursor，用来调用SQL语句对数据库进行操作
c = conn.cursor()
# 创建数据表,SQLite未实现表的替换功能，若数据库文件不为空，则此句报错
c.execute('create table info_db (name, gender, age)')
# 插入一条信息
c.execute("insert into info_db (name, gender, age) values ('jk', 'male', 18)")
c.execute('select * from info_db')
c.execute('select * from info_db')
# 输出所有的查询结果
print(c.fetchall())
'''
[('jk', 'male', 18), ('jk', 'male', 18)]
'''
# 保存对数据库的修改
conn.commit()
conn.close()