from graph import DagGraph
import glob
from helper import SqlHelper


dg = DagGraph()

sql_file_path = '/Users/dupeng/IdeaProjects/duperl/daas-migration/daas-backup'

sql_files = glob.glob(sql_file_path + '/数字运营_经营看板任务5_业绩顾客任务/*.sql')

sql_stmt_str = ""
for sql_file in sql_files:
    sql_str = open(sql_file, 'r').read()
    if not sql_str.strip().endswith(';\n'):
        sql_str = sql_str + '\n;\n'
    sql_stmt_str += sql_str

print(sql_stmt_str)
sql_stmt_lst = SqlHelper.split(sql_stmt_str)

for sql_stmt in sql_stmt_lst:
    # print(sql_stmt)
    x = SqlHelper.get_source_target_tables(sql_stmt)
    if x:
        # print(x)
        target_tables = x['target_table']
        source_tables = x['source_table']
        for source_table in source_tables:
            for target_table in target_tables:
                dg.add_edge(source_table, target_table)

# dg.print_related_edges_backward('dwd_hive.dwd_member_relation')

dg.print_all_edges()