from helper import SqlHelper


sql = """
-- select 123; -- ok
  # 注释 
select '#77'# 注释。。。
"""



sql = SqlHelper.trim_single_line_comment(sql)

print(sql)