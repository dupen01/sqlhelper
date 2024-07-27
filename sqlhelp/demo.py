

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
