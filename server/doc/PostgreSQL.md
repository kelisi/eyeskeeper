# PostgreSQL

## 1.进入sql控制终端

```shell
psql
#创建用户
CREATE USER test WITH PASSWORD 'test';

CREATE USER "123" WITH
	LOGIN
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	REPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxx';

GRANT pg_monitor TO "123";

#创建用户数据库
CREATE DATABASE testdb OWNER test;
#将数据库的所有权限都赋予用户，否则dbuser只能登录控制台，没有任何数据库操作权限。
GRANT ALL PRIVILEGES ON DATABASE testdb to test;
#退出控制终端
\q
```

控制台指令

```
\h：查看SQL命令的解释，比如\h select。
\?：查看psql命令列表。
\l：列出所有数据库。
\c [database_name]：连接其他数据库。
\d：列出当前数据库的所有表格。
\d [table_name]：列出某一张表格的结构。
\du：列出所有用户。
\e：打开文本编辑器。
\conninfo：列出当前数据库和连接的信息。
```



## 2.连接数据库

```shell
psql -U test -d testdb -h 127.0.0.1 -p 5432
```

### 3.查询数据库中的所有表

```shell
\d
#若出现Did not find any relations.错误可使用以下几种
#1 https://stackoverflow.com/questions/7758533/postgresql-database-owner-cant-access-database-no-relations-found/7758860#7758860
grant all on schema public to public;
#2
\dt *.*

```



## 3.操作数据库

```mariadb
# 创建新表 
CREATE TABLE user_tbl(name VARCHAR(20), signup_date DATE);

# 插入数据 
INSERT INTO user_tbl(name, signup_date) VALUES('张三', '2013-12-22');

# 选择记录 
SELECT * FROM user_tbl;

# 更新数据 
UPDATE user_tbl set name = '李四' WHERE name = '张三';

# 删除记录 
DELETE FROM user_tbl WHERE name = '李四' ;

# 添加栏位 
ALTER TABLE user_tbl ADD email VARCHAR(40);

# 更新结构 
ALTER TABLE user_tbl ALTER COLUMN signup_date SET NOT NULL;

# 更名栏位 
ALTER TABLE user_tbl RENAME COLUMN signup_date TO signup;

# 删除栏位 
ALTER TABLE user_tbl DROP COLUMN email;

# 表格更名 
ALTER TABLE user_tbl RENAME TO backup_tbl;

# 删除表格 
DROP TABLE IF EXISTS backup_tbl;


```

