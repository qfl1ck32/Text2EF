from typing import List
import sqlparse

from helpers import remove_whitespaces
from builder import select_clause_builder, where_clause_builder, from_clause_builder


class SelectAstBuilder:
    @staticmethod
    def __find_clause_indexes(tokens: List[sqlparse.sql.Token]):
        select_start = None
        from_start = None
        where_start = None
        for (index, token) in enumerate(tokens):
            if token.ttype == sqlparse.tokens.DML and token.normalized == 'SELECT':
                select_start = index
            elif token.ttype == sqlparse.tokens.Keyword and token.normalized == 'FROM':
                from_start = index
            elif isinstance(token, sqlparse.sql.Where):
                where_start = index

        return select_start, from_start, where_start

    @staticmethod
    def build(sql: str):
        statements = sqlparse.parse(sql)

        if len(statements) != 1:
            raise ValueError('SQL should contain only one statement')

        tokens = remove_whitespaces(statements[0].tokens)

        [select_index, from_index,
            where_index] = SelectAstBuilder.__find_clause_indexes(tokens)

        select_tokens = tokens[select_index: from_index]
        from_tokens = tokens[from_index: where_index]
        where_tokens = tokens[where_index:]

        select_clause = select_clause_builder.get_select_clause(select_tokens)
        from_clause = from_clause_builder.get_from_clause(from_tokens)
        where_clause = where_clause_builder.get_where_clause(where_tokens[0])

        return {
            select_clause,
            from_clause,
            where_clause
        }
