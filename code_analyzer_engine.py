import re
from typing import List
from utils import read_contents_of_all_files, extract_line_number, extract_name_from_declaration

LINE_TOO_LONG_CODE = "S001 Too long"
WRONG_INDENTATION_CODE = "S002 Indentation is not a multiple of four"
WRONG_SEMICOLON_CODE = "S003 Unnecessary semicolon"
MISSING_SPACE_BEFORE_COMMEND_CODE = "S004 At least two spaces required before inline comments"
TODO_FOUND_CODE = "S005 TODO found"
WRONG_BLANK_LINES_CODE = "S006 More than two blank lines used before this line"
TOO_MANY_SPACES_AFTER_DECLARATION_CODE = "S007 Too many spaces after"
CAMEL_CASE_CODE = "S008"
SNAKE_CASE_CODE = "S009"

TODO = "todo"
CLASS = "class"
FUNCTION = "def"

SPACES_AFTER_CLASS_REGEX = rf" *{CLASS} \w+"
SPACES_AFTER_DEF_REGEX = rf" *{FUNCTION} \w+"
CAMEL_CASE_REGEX = r"[A-Z][A-Za-z0-9]*\b"
SNAKE_CASE_REGEX = r"_{0,2}[a-z](_?[a-z0-9])*_{0,2}\b"


class CodeAnalyzerEngine:

    def __init__(self, file_name: str):
        self.files = read_contents_of_all_files(file_name)

    def analyze_code(self) -> List[str]:
        errors_found = []
        for file_name in self.files:
            errors_for_file = []
            errors_for_file += self.check_line_length(file_name)
            errors_for_file += self.check_indentation(file_name)
            errors_for_file += self.check_comments(file_name)
            errors_for_file += self.check_blank_lines(file_name)
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

    def check_naming(self, file_name: str) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.files[file_name]):
            if re.match(rf" *{CLASS}\b", line) is not None:
                errors_found += _handle_naming_of_class(file_name, line_number, line)
            elif re.match(rf" *{FUNCTION}\b", line) is not None:
                errors_found += _handle_naming_of_function(file_name, line_number, line)
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


def _handle_naming_of_class(file_name: str, line_number: int, line: str):
    error_messages = []
    if re.match(SPACES_AFTER_CLASS_REGEX, line) is None:
        error_messages.append(
            f"{file_name}: Line {line_number + 1}: {TOO_MANY_SPACES_AFTER_DECLARATION_CODE} '{CLASS}'")

    # we only check class name, not spaces before ":" or name of parent class
    class_name = extract_name_from_declaration(line)

    if re.match(CAMEL_CASE_REGEX, class_name) is None:
        error_messages.append(
            f"{file_name}: Line {line_number + 1}: "
            f"{CAMEL_CASE_CODE} Class name '{class_name}' should use CamelCase")
    return error_messages


def _handle_naming_of_function(file_name: str, line_number: int, line: str):
    error_messages = []
    if re.match(SPACES_AFTER_DEF_REGEX, line) is None:
        error_messages.append(
            f"{file_name}: Line {line_number + 1}: {TOO_MANY_SPACES_AFTER_DECLARATION_CODE} '{FUNCTION}'")

    # we only check class name, not spaces before ":" or name of parent class
    function_name = extract_name_from_declaration(line)

    if re.match(SNAKE_CASE_REGEX, function_name) is None:
        error_messages.append(
            f"{file_name}: Line {line_number + 1}: "
            f"{SNAKE_CASE_CODE} Function name '{function_name}' should use snake_case")
    return error_messages
