import re

SPACES_AFTER_DECLARATION_REGEX = r" *(class|def) {2,}\w+"
SNAKE_CASE_REGEX = r"_{0,2}[a-z](_?[a-z0-9])*_{0,2}\b"
CAMEL_CASE_REGEX = r"[A-Z][A-Za-z0-9]*\b"


def are_too_many_spaces_after_declaration(line: str) -> bool:
    if re.match(SPACES_AFTER_DECLARATION_REGEX, line) is not None:
        return True
    else:
        return False


def is_snake_case(name: str) -> bool:
    if re.match(SNAKE_CASE_REGEX, name) is None:
        return False
    else:
        return True


def is_camel_case(name: str) -> bool:
    if re.match(CAMEL_CASE_REGEX, name) is None:
        return False
    else:
        return True



