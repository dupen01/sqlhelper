from typing import List
from keywords import KeyWords
import re 


class ParseException(Exception):
    pass


class SqlHelper:
    @staticmethod
    def split(sql: str) -> List[str]:
        """将多条SQL分隔为列表"""
        result = []
        # 嵌套注释的层级数
        multi_comment_level = 0
        # 多行SQL的前缀语句,分号之前的语句
        prefix = ""
        sql = sql + ';' if not sql.strip().endswith(';') else sql
        for line in sql.splitlines():
            line = line if not line.strip().startswith('--') else ''
            # 标记是否以双引号结尾
            has_terminated_double_quote = True
            # 标记是否以单引号结尾
            has_terminated_single_quote = True
            # 标记是否属于单行注释内容
            is_single_line_comment = False
            # 标记前一个字符是否是短横行 "-"
            was_pre_dash = False
            # 标记前一个字符是否是斜杆 "/"
            was_pre_slash = False
            # 标记前一个字符是否是星号 "*"
            was_pre_star = False
            last_semi_index = 0
            index = 0
            if len(prefix) > 0:
                prefix += "\n"
            for char in line:
                index += 1
                match char:
                    case "'":
                        if has_terminated_double_quote:
                            has_terminated_single_quote = not has_terminated_single_quote
                    case '"':
                        if has_terminated_single_quote:
                            has_terminated_double_quote = not has_terminated_double_quote
                    case '-':
                        if has_terminated_double_quote and has_terminated_single_quote:
                            if was_pre_dash:
                                is_single_line_comment = True
                        was_pre_dash = True
                    case '/':
                        if has_terminated_double_quote and has_terminated_single_quote:
                            # 如果'/'前面是'*'， 那么嵌套层级数-1
                            if was_pre_star:
                                multi_comment_level -= 1
                        was_pre_slash = True
                        was_pre_dash = False
                        was_pre_star = False
                    case '*':
                        if has_terminated_double_quote and has_terminated_single_quote:
                            # 如果'*'前面是'/'， 那么嵌套层级数+1
                            if was_pre_slash:
                                multi_comment_level += 1
                        was_pre_star = True
                        was_pre_dash = False
                        was_pre_slash = False
                    case ';':
                        # 当分号不在单引号内，不在双引号内，不属于单行注释，并且多行嵌套注释的层级数为0时，表示此分号应该作为分隔符进行划分
                        if (has_terminated_double_quote and
                                has_terminated_single_quote and
                                not is_single_line_comment and
                                multi_comment_level == 0):
                            sql_stmt = prefix + line[last_semi_index:index-1]
                            result.append(sql_stmt)
                            prefix = ""
                            last_semi_index = index
                    case _:
                        was_pre_dash = False
                        was_pre_slash = False
                        was_pre_star = False
            if last_semi_index != index or len(line) == 0:
                prefix += line[last_semi_index:]
        assert multi_comment_level == 0, (f"The number of nested levels of sql multi-line comments is not equal to 0: "
                                          f"{multi_comment_level}")
        return result


    @staticmethod
    def trim_comment(sql: str) -> str:
        """删除注释"""
        result = []
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.M | re.S)
        for line in sql.splitlines():
            line = line if not line.strip().startswith('--') else ''
            # 标记是否以双引号结尾
            has_terminated_double_quote = True
            # 标记是否以单引号结尾
            has_terminated_single_quote = True
            # 标记前一个字符是否是短横行 "-"
            was_pre_dash = False
            index = 0
            for char in line:
                index += 1
                match char:
                    case "'":
                        if has_terminated_double_quote:
                            has_terminated_single_quote = not has_terminated_single_quote
                    case '"':
                        if has_terminated_single_quote:
                            has_terminated_double_quote = not has_terminated_double_quote
                    case '-':
                        if has_terminated_double_quote and has_terminated_single_quote:
                            if was_pre_dash:
                                line = line[:index-2]
                                continue
                        was_pre_dash = True
                    case _:
                        was_pre_dash = False
            result.append(line)
        return '\n'.join(result)


    @staticmethod
    def get_cte_mid_tables(sql: str) -> list:
        """获取cte语句的临时表名"""
        # 括号层级
        bracket_level = 0
        was_pre_with = False
        is_cte = False
        was_pre_right_bracket = False
        result = []

        # 预处理：去掉多行注释和单行注释
        sql = SqlHelper.trim_comment(sql)

        for line in sql.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue
            
            line = line.replace('(', ' ( ')
            line = line.replace(')', ' ) ')
            line = line.replace(',', ' , ')

            for token in line.split(' '):
                token = token.strip()
                if len(token) == 0:
                    continue
                if token.upper() == '(':
                    bracket_level += 1
                if token.upper() == ')':
                    bracket_level -= 1
                    was_pre_right_bracket = True
                if token.upper() == 'WITH':
                    was_pre_with = True
                    is_cte = True

                if token.upper() in KeyWords.keywords:
                    if was_pre_right_bracket and is_cte and bracket_level == 0 and token.upper() != 'AS':
                        is_cte = False
                        
                if token.upper() not in KeyWords.keywords:
                    if was_pre_with:
                        result.append(token)
                    if is_cte and bracket_level == 0 and not was_pre_with and token not in (',', '(', ')'):
                        result.append(token)
                    was_pre_with = False
        return result


    @staticmethod
    def get_source_target_tables(sql: str) -> dict:
        """传入一个SQL语句，输出这条SQL的来源表和目标表名，可用于表级血缘关系梳理
        标记 source 表和 target 表：
        source 表：FROM 和 JOIN 后面的词
        TODO 暂未支持嵌套CTE语句
        """
        # 校验SQL参数
        if len(SqlHelper.split(sql)) > 1:
            raise ParseException("sql脚本为多条SQL语句,需传入单条SQL语句.")

        was_pre_insert = False
        was_pre_from = False
        was_pre_as = False
        was_pre_table_name = False
        target_table = ''
        source_table = []
        result = {}

        # 预处理：去掉多行注释和单行注释
        sql = SqlHelper.trim_comment(sql)

        for line in sql.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue
            
            line = line.replace('(', ' ( ')
            line = line.replace(')', ' ) ')
            line = line.replace(',', ' , ')

            for token in line.split(' '):
                token = token.strip()
                if len(token) == 0:
                    continue

                if token.upper() == 'AS':
                    was_pre_as = True
                    continue

                if token.upper() in KeyWords.insert_keywords:
                    was_pre_insert = True
                    was_pre_from = False
                    continue

                if token.upper() in KeyWords.from_keywords:
                    was_pre_from = True
                    was_pre_insert = False
                    was_pre_table_name = False
                    continue

                if was_pre_as and token.upper() not in KeyWords.keywords:
                    was_pre_as = False
                    was_pre_table_name = False
                    continue

                if token.upper() in KeyWords.keywords:
                    if was_pre_insert or was_pre_from:
                        was_pre_from = False
                    continue

                if token.upper() not in KeyWords.keywords and was_pre_insert:
                    target_table = token
                    was_pre_insert = False
                    was_pre_from = False
                    continue

                if was_pre_from:
                    if token not in KeyWords.keywords and not was_pre_table_name and token not in (',', '('):
                        source_table.append(token)
                        was_pre_from = True
                        was_pre_table_name = True
                    if token in ['AS', ',']:
                        was_pre_from = True
                        was_pre_table_name = False

        mid_table = SqlHelper.get_cte_mid_tables(sql)
        source_table = list(set(source_table) - set(mid_table))
        if len(source_table) != 0:
            result.setdefault('target_table', target_table)
            result.setdefault('source_table', source_table)
            return result
        else:
            return
