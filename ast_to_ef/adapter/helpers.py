# TODO: it should use clang-format instead of autopep8
import autopep8


def format_code(code: str) -> str:
    return autopep8.fix_code(code, options={"aggressive": 1})
