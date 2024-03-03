import sqlparse

from typing import List

from helpers import clean_tokens
from models import field, condition


__condition_logical_operators_precedence = {
    condition.ConditionLogicalOperator.OR.value: 1,
    condition.ConditionLogicalOperator.AND.value: 2,
    condition.ConditionLogicalOperator.NOT.value: 3
}

__condition_logical_operators = [
    condition.ConditionLogicalOperator.AND.value,
    condition.ConditionLogicalOperator.OR.value,
    condition.ConditionLogicalOperator.NOT.value,
]


def get_conditions(token: sqlparse.sql.Token):
    if type(token) != sqlparse.sql.Where:
        raise ValueError(f"Expected WHERE, got {token}")

    return __build_where_ast(token.tokens[1:])


# TODO: If we have WHERE "a" = 1, because of the double quotes, it's a field, not a string. If using single quotes, it's ok. This is weird
def __construct_operand(token: sqlparse.sql.Token) -> condition.ConditionOperand:
    if isinstance(token, sqlparse.sql.Identifier):
        return field.Field(
            name=token.get_real_name(),
            alias=token.get_alias(),
            parent=token.get_parent_name()
        )
    elif token.ttype == sqlparse.tokens.Literal.Number.Integer:
        return condition.IntOperand(value=int(token.value))
    elif token.ttype == sqlparse.tokens.Literal.Number.Float:
        return condition.FloatOperand(value=float(token.value))
    elif token.ttype == sqlparse.tokens.Literal.String.Single:
        return condition.StringOperand(value=token.value[1:-1])
    else:
        raise ValueError(f"Unsupported token: {token}")


def __build_condition(token: sqlparse.sql.Token) -> condition.Condition:
    if not isinstance(token, sqlparse.sql.Comparison):
        raise ValueError(f"Expected comparison, got {token}")

    cleaned: List[sqlparse.sql.Token] = clean_tokens(token.tokens)

    if len(cleaned) != 3:
        raise ValueError(
            f"Expected 3 tokens, got: {len(cleaned)} [{(cleaned,)}]")

    [left, operator, right] = cleaned

    # TODOO: Check for subqueries
    return condition.Condition(
        left=__construct_operand(left),
        operator=condition.ConditionOperator.from_string(operator.value),
        right=__construct_operand(right)
    )


def __build_where_ast(tokens: List[sqlparse.sql.Token]) -> condition.ConditionLogicalExpression | condition.Condition:
    tokens = clean_tokens(tokens)

    if len(tokens) == 1:
        [token] = tokens
        return __build_condition(token)

    operator_stack: List[str] = []
    operand_stack: List[condition.ConditionLogicalExpression |
                        condition.Condition] = []

    for token in tokens:
        if token.ttype == sqlparse.tokens.Keyword and token.value.upper() in __condition_logical_operators:
            while operator_stack and __condition_logical_operators_precedence[operator_stack[-1]] >= __condition_logical_operators_precedence[token.value.upper()]:
                operator = operator_stack.pop()
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()
                operand_stack.append(
                    condition.ConditionLogicalExpression(
                        left=left_operand,
                        operator=condition.ConditionLogicalOperator.from_string(
                            operator),
                        right=right_operand
                    )
                )
            operator_stack.append(token.value.upper())
        elif isinstance(token, sqlparse.sql.Parenthesis):
            sub_conditions = __build_where_ast(
                clean_tokens(token.tokens)[1:-1])

            operand_stack.append(sub_conditions)
        else:
            operand_stack.append(__build_condition(token))

    while operator_stack:
        operator = operator_stack.pop()
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()
        operand_stack.append(
            condition.ConditionLogicalExpression(
                left=left_operand,
                operator=condition.ConditionLogicalOperator.from_string(
                    operator),
                right=right_operand
            )
        )

    return operand_stack[0]
