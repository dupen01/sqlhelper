from helper import SqlHelper


sql1 = """
insert into ods.t1
select * from ods.t2;
"""

sql2 = """
insert overwrite table ods.t1
select * from ods.t2;
"""

sql3 = """
update ods.t1
set a = b
where 1=1
"""

sql4 = """
create view t_v as 
select * from ods.t2;
"""

sql5 = """
merge into dwd.t1
using ods_t2 t2
on 1=1
when matched then
update a= b
"""

sql6 = """
merge into dwd.t1 t1
using (select * from t3) t2
on 1=1
when matched then
update a= b
"""

rs = SqlHelper.get_source_target_tables(sql5)

print(rs)