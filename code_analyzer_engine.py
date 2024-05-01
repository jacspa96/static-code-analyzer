import re
import ast
from typing import List
from regex_utils import (are_too_many_spaces_after_declaration,
                         is_snake_case,
                         is_camel_case)
from file_utils import (read_contents_of_all_files,
                        read_code_trees_of_all_files,
                        extract_line_number,
                        extract_name_from_declaration)

LINE_TOO_LONG_CODE = "S001 Too long"
WRONG_INDENTATION_CODE = "S002 Indentation is not a multiple of four"
WRONG_SEMICOLON_CODE = "S003 Unnecessary semicolon"
MISSING_SPACE_BEFORE_COMMEND_CODE = "S004 At least two spaces required before inline comments"
TODO_FOUND_CODE = "S005 TODO found"
WRONG_BLANK_LINES_CODE = "S006 More than two blank lines used before this line"
TOO_MANY_SPACES_AFTER_DECLARATION_CODE = "S007 Too many spaces after"
CAMEL_CASE_CODE = "S008"
SNAKE_CASE_FUN_CODE = "S009"
SNAKE_CASE_ARG_CODE = "S010"
SNAKE_CASE_VAR_CODE = "S011"
MUTABLE_DEFAULT_CODE = "S012 Default argument value is mutable"

TODO = "todo"
CLASS = "class"
FUNCTION = "def"

MUTABLE_DATA_TYPES = (ast.List, ast.Set, ast.Dict)

class CodeAnalyzerEngine:

    def __init__(self, path: str):
        self.files = read_contents_of_all_files(path)
        self.code_trees = read_code_trees_of_all_files(path)

    def analyze_code(self) -> List[str]:
        errors_found = []
        for file_name in self.files:
            errors_for_file = []
            errors_for_file += self.check_line_length(file_name)
            errors_for_file += self.check_indentation(file_name)
            errors_for_file += self.check_comments(file_name)
            errors_for_file += self.check_blank_lines(file_name)
            errors_for_file += self.check_spaces_after_declaration(file_name)
            errors_for_file += self.check_naming(file_name)
            errors_for_file.sort(key=lambda error_message: extract_line_number(error_message))
            errors_found += errors_for_file
        return errors_found

    def check_line_length(self, file_name: str) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.files[file_name]):
            if len(line) > 79:
                errors_found.append(f"{file_name}: Line {line_number + 1}: {LINE_TOO_LONG_CODE}")
        return errors_found

    def check_indentation(self, file_name: str) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.files[file_name]):
            if (len(line) - len(line.lstrip(" "))) % 4 != 0:
                errors_found.append(f"{file_name}: Line {line_number + 1}: {WRONG_INDENTATION_CODE}")
        return errors_found

    def check_comments(self, file_name: str) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.files[file_name]):
            if "#" in line:
                error_messages = _handle_line_with_comment(file_name, line_number, line)
            else:
                error_messages = _handle_line_without_comment(file_name, line_number, line)
            errors_found += error_messages
        return errors_found

    def check_blank_lines(self, file_name: str) -> List[str]:
        errors_found = []
        blank_lines_counter = 0
        for line_number, line in enumerate(self.files[file_name]):
            if len(line.strip()) == 0:
                blank_lines_counter += 1
            elif blank_lines_counter <= 2:
                blank_lines_counter = 0
            else:
                errors_found.append(f"{file_name}: Line {line_number + 1}: {WRONG_BLANK_LINES_CODE}")
                blank_lines_counter = 0
        return errors_found

    def check_spaces_after_declaration(self, file_name: str) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.files[file_name]):
            if are_too_many_spaces_after_declaration(line):
                declaration_keyword = line.split()[0]
                errors_found.append(
                    f"{file_name}: Line {line_number + 1}: "
                    f"{TOO_MANY_SPACES_AFTER_DECLARATION_CODE} '{declaration_keyword}'"
                )
        return errors_found

    def check_naming(self, file_name: str) -> List[str]:
        errors_found = []
        for node in ast.walk(self.code_trees[file_name]):
            if isinstance(node, ast.ClassDef):
                errors_found += _check_class_style(file_name, node)
            elif isinstance(node, ast.FunctionDef):
                errors_found += _check_function_style(file_name, node)
            elif isinstance(node, ast.Assign):
                errors_found += _check_variable_style(file_name, node)

        return errors_found


def _handle_line_with_comment(file_name: str, line_number: int, line: str) -> List[str]:
    error_messages = []
    code, comment = line.split("#", maxsplit=1)
    error_messages += _handle_line_without_comment(file_name, line_number, code)
    if len(code) != 0 and (len(code) - len(code.rstrip())) < 2:
        error_messages.append(f"{file_name}: Line {line_number + 1}: {MISSING_SPACE_BEFORE_COMMEND_CODE}")
    if TODO in comment.lower():
        error_messages.append(f"{file_name}: Line {line_number + 1}: {TODO_FOUND_CODE}")
    return error_messages


def _handle_line_without_comment(file_name: str, line_number: int, line: str) -> List[str]:
    line = line.replace(" ", "")
    if len(line) != 0 and line[-1] == ";":
        return [f"{file_name}: Line {line_number + 1}: {WRONG_SEMICOLON_CODE}"]
    return []


def _check_class_style(file_name: str, node: ast.ClassDef) -> List[str]:
    error_message = []
    line_number = node.lineno

    class_name = node.name
    if not is_camel_case(class_name):
        error_message.append(
            f"{file_name}: Line {line_number}: "
            f"{CAMEL_CASE_CODE} Class name '{class_name}' should use CamelCase"
        )

    return error_message


def _check_function_style(file_name: str, node: ast.FunctionDef) -> List[str]:
    error_message = []
    line_number = node.lineno

    function_name = node.name
    if not is_snake_case(function_name):
        error_message.append(
            f"{file_name}: Line {line_number}: "
            f"{SNAKE_CASE_FUN_CODE} Function name '{function_name}' should use snake_case"
        )

    arguments = node.args.args
    for argument in arguments:
        argument_name = argument.arg
        if not is_snake_case(argument_name):
            error_message.append(
                f"{file_name}: Line {line_number}: "
                f"{SNAKE_CASE_ARG_CODE} Argument name '{argument_name}' should be snake_case"
            )

    defaults = node.args.defaults
    for default in defaults:
        if isinstance(default, MUTABLE_DATA_TYPES):
            error_message.append(
                f"{file_name}: Line {line_number}: {MUTABLE_DEFAULT_CODE}"
            )

    # function_body = node.body
    # for inner_node in function_body:
    #     if isinstance(inner_node, ast.Assign):
    #         error_message += _check_variable_style(file_name, inner_node)

    return error_message


def _check_variable_style(file_name: str, node: ast.Assign) -> List[str]:
    error_message = []
    line_number = node.lineno

    variables = node.targets
    for variable in variables:
        if isinstance(variable, ast.Name):
            variable_name = variable.id
            if not is_snake_case(variable_name):
                error_message.append(
                    f"{file_name}: Line {line_number}: "
                    f"{SNAKE_CASE_VAR_CODE} Variable '{variable_name}' should be snake_case"
                )

    return error_message




