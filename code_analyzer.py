import sys
from typing import List


LINE_TOO_LONG_CODE = "S001 Too long"


def main():
    file_name = input()
    errors = analyze_code(file_name)
    print(*errors, sep="\n")


def analyze_code(file_name: str) -> List[str]:
    errors_found = []
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f]
    for line_number, line in enumerate(lines):
        if len(line) > 79:
            errors_found.append(f"Line {line_number+1}: {LINE_TOO_LONG_CODE}")
    return errors_found


if __name__ == '__main__':
    main()
