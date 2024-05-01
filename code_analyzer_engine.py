from typing import List
from utils import read_contents_of_all_files, extract_line_number

LINE_TOO_LONG_CODE = "S001 Too long"
WRONG_INDENTATION_CODE = "S002 Indentation is not a multiple of four"
WRONG_SEMICOLON_CODE = "S003 Unnecessary semicolon"
MISSING_SPACE_BEFORE_COMMEND_CODE = "S004 At least two spaces required before inline comments"
TODO_FOUND_CODE = "S005 TODO found"
WRONG_BLANK_LINES_CODE = "S006 More than two blank lines used before this line"

TODO = "todo"


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
                error_messages = self._handle_line_with_comment(file_name, line_number, line)
            else:
                error_messages = self._handle_line_without_comment(file_name, line_number, line)
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

    @staticmethod
    def _handle_line_with_comment(file_name: str, line_number: int, line: str) -> List[str]:
        error_messages = []
        code, comment = line.split("#", maxsplit=1)
        error_messages += CodeAnalyzerEngine._handle_line_without_comment(file_name, line_number, code)
        if len(code) != 0 and (len(code) - len(code.rstrip())) < 2:
            error_messages.append(f"{file_name}: Line {line_number + 1}: {MISSING_SPACE_BEFORE_COMMEND_CODE}")
        if TODO in comment.lower():
            error_messages.append(f"{file_name}: Line {line_number + 1}: {TODO_FOUND_CODE}")
        return error_messages

    @staticmethod
    def _handle_line_without_comment(file_name: str, line_number: int, line: str) -> List[str]:
        line = line.replace(" ", "")
        if len(line) != 0 and line[-1] == ";":
            return [f"{file_name}: Line {line_number + 1}: {WRONG_SEMICOLON_CODE}"]
        return []
