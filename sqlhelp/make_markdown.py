from sql_helper import SqlHelper


def _dict_to_mermaid(res: dict):
    result = []
    target_table = res.get('target_table')
    source_tables = res.get('source_table')
    for table in source_tables:
        result.append(f"{table} --> {target_table}")
    return '\n'.join(result)


def get_sql_from_file(file_path):
    import glob
    total_sql = []
    files = glob.glob(file_path)
    for file in files:
        with open(file, 'r') as f:
            sql = f.read()
            if not sql.strip().endswith(';'):
                sql = sql + ';'
            total_sql.append(sql)
    return '\n'.join(total_sql)


def sql_to_mermaid(total_sql):
    total_mermaid = []
    sql_lst = SqlHelper.split(total_sql)
    for sql in sql_lst:
        res = SqlHelper.get_source_target_tables(sql)
        if res:
            total_mermaid.append(_dict_to_mermaid(res))

    return '\n'.join(list(set(total_mermaid)))


if __name__ == '__main__':
    total_sql = get_sql_from_file('sqlhelp/sql-files/*.sql')
    mermaid_str = sql_to_mermaid(total_sql)
    prefix = "graph LR\n"
    print(prefix, mermaid_str)
