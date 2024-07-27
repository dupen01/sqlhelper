from sql_helper import SqlHelper


def to_markdown(res: dict):
    markdown_lst = []
    target_table = res.get('target_table')
    source_tables = res.get('source_table')
    for table in source_tables:
        markdown_lst.append(f"{table} --> {target_table}")
    return markdown_lst


markdown_lst = []

total_sql = []

import glob
sql_files = glob.glob('sqlhelp/sql-files/*.sql')
sql_files = glob.glob('sqlhelp/sql-files/query02.sql')

for file in sql_files:
    with open(file, 'r') as f:
        total_sql.append(f.read())

total_sql_str = '\n'.join(total_sql)

sql_lst = SqlHelper.split(total_sql_str)

for sql in sql_lst:
    # print(sql)
    res = SqlHelper.get_source_target_tables(sql)
    if res:
        md_lst = to_markdown(res)
        markdown_lst.extend(md_lst)
    

markdown_str = '\n'.join(list(set(markdown_lst)))
markdown_str = 'graph LR\n' + markdown_str
print(len(list(set(markdown_lst))))
print(markdown_str)