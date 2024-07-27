from sql_helper import SqlHelper

# result = {'target_table': 'dws_hive.dws_last_thirty_days_shop_risk_warning', 'source_table': ['dwd_hive.dwd_last_thirty_days_shop_manual', 'dwd_hive.dwd_last_thirty_days_shop_use_coupon', 'dwd_hive.dwd_last_thirty_days_shop_collection_on_behalf', 'dwd_hive.dwd_last_thirty_days_shop_real_refund', 'dwd_hive.dwd_last_thirty_days_shop_real_refund', 'dwd_hive.dwd_last_thirty_days_shop_extract_staff_count', 'dwd_hive.dwd_last_thirty_days_shop_manual', 'dwd_hive.dwd_shop_risk_warn_allot', 'ods_hive.ods_risk_warning_config', 'dwd_hive.dwd_shop_risk_warn_order_and_consume', 'ods_hive.ods_risk_warning_config', 'dwd_hive.dwd_xy_sr_order_receipt_detail', 'dwd_hive.dwd_xy_shop_performance_report', 'dwd_hive.dwd_xy_sr_order_receipt_detail', 'dwd_hive.dwd_xy_shop_performance_report', 'dwd_hive.dwd_xy_sr_order_receipt_detail']}
# result = {'target_table': 'dws_hive.dws_last_thirty_days_shop_risk_warning', 'source_table': []}

def get_sql():
    ...


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
sql_files = glob.glob('/Users/dupeng/IdeaProjects/duperl/exec-sql/starrocks-sql/dass-backup/预约看板/*.sql')
# sql_files = glob.glob('/Users/dupeng/IdeaProjects/duperl/exec-sql/starrocks-sql/dass-backup/数字运营_v1_DWS/*.sql')
# sql_files = glob.glob('/Users/dupeng/IdeaProjects/duperl/exec-sql/starrocks-sql/dass-backup/任务主题/*.sql')
# sql_files = glob.glob('/Users/dupeng/IdeaProjects/duperl/exec-sql/starrocks-sql/dass-backup/市场部看板_全量/*.sql')
# sql_files = glob.glob('/Users/dupeng/IdeaProjects/duperl/exec-sql/starrocks-sql/dass-backup/*/*.sql')

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