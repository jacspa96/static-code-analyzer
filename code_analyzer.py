from typing import List

LINE_TOO_LONG_CODE = "S001 Too long"
WRONG_INDENTATION_CODE = "S002 Indentation is not a multiple of four"
WRONG_SEMICOLON_CODE = "S003 Unnecessary semicolon"
MISSING_SPACE_BEFORE_COMMEND_CODE = "S004 At least two spaces required before inline comments"
TODO_FOUND_CODE = "S005 TODO found"
WRONG_BLANK_LINES_CODE = "S006 More than two blank lines used before this line"

TODO = "todo"


class CodeAnalyzer:

    def __init__(self, file_name: str):
        self.lines = read_lines_from_file(file_name)

    def analyze_code(self) -> List[str]:
        errors_found = []
        errors_found += self.check_line_length()
        errors_found += self.check_indentation()
        errors_found += self.check_comments()
        errors_found += self.check_blank_lines()
        return sorted(errors_found,
                      key=lambda error_message: self._extract_line_number(error_message))

    def check_line_length(self) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.lines):
            if len(line) > 79:
                errors_found.append(f"Line {line_number + 1}: {LINE_TOO_LONG_CODE}")
        return errors_found

    def check_indentation(self) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.lines):
            if (len(line) - len(line.lstrip(" "))) % 4 != 0:
                errors_found.append(f"Line {line_number + 1}: {WRONG_INDENTATION_CODE}")
        return errors_found

    def check_comments(self) -> List[str]:
        errors_found = []
        for line_number, line in enumerate(self.lines):
            if "#" in line:
                error_messages = self._handle_line_with_comment(line_number, line)
            else:
                error_messages = self._handle_line_without_comment(line_number, line)
            errors_found += error_messages
        return errors_found

    def check_blank_lines(self) -> List[str]:
        errors_found = []
        blank_lines_counter = 0
        for line_number, line in enumerate(self.lines):
            if len(line.strip()) == 0:
                blank_lines_counter += 1
            elif blank_lines_counter <= 2:
                blank_lines_counter = 0
            else:
                errors_found.append(f"Line {line_number + 1}: {WRONG_BLANK_LINES_CODE}")
                blank_lines_counter = 0
        return errors_found

    @staticmethod
    def _handle_line_with_comment(line_number: int, line: str) -> List[str]:
        error_messages = []
        code, comment = line.split("#", maxsplit=1)
        error_messages += CodeAnalyzer._handle_line_without_comment(line_number, code)
        if len(code) != 0 and (len(code) - len(code.rstrip())) < 2:
            error_messages.append(f"Line {line_number + 1}: {MISSING_SPACE_BEFORE_COMMEND_CODE}")
        if TODO in comment.lower():
            error_messages.append(f"Line {line_number + 1}: {TODO_FOUND_CODE}")
        return error_messages

    @staticmethod
    def _handle_line_without_comment(line_number: int, line: str) -> List[str]:
        line = line.replace(" ", "")
        if len(line) != 0 and line[-1] == ";":
            return [f"Line {line_number + 1}: {WRONG_SEMICOLON_CODE}"]
        return []

    @staticmethod
    def _extract_line_number(message: str):
        return int(message.split(":")[0].split()[1])


def main():
    file_name = input()
    code_analyzer = CodeAnalyzer(file_name)
    errors = code_analyzer.analyze_code()
    print(*errors, sep="\n")


def read_lines_from_file(file_name: str) -> List[str]:
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f]
    return lines


if __name__ == '__main__':
    main()
