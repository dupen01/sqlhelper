

sql = """
select id  /*ooo
注释1
aaa
/* 嵌套
注释 */
bbb
*/
select /*+ SQL Hint */ 
id, -- ID
'/*假注释*/' as hehe,
'-- ooo' as haha,
name 
from t3 /*注释2*/ ded
"""


from sql_helper import SqlHelper
sql = SqlHelper.trim_comment(sql)


print(sql)


sql2 = """
create database if exists ods;
-- as select * from bbb
"""
print(SqlHelper.split(sql2))
print(SqlHelper.get_source_target_tables(sql2))
