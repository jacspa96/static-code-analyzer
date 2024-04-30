import os
from typing import List


MESSAGE_PARTS_SEPARATOR = ": "
LINE_INFO_POSITION = 1
LINE_NUMBER_POSITION = 1


def extract_line_number(message: str):
    line_info = message.split(MESSAGE_PARTS_SEPARATOR)[LINE_INFO_POSITION]
    line_number = int(line_info.split(" ")[LINE_NUMBER_POSITION])
    return line_number


def read_contents_of_all_files(path: str) -> dict:
    if os.path.isfile(path):
        return {path: _read_lines_from_file(path)}
    else:
        return _crawl_over_directory(path)


def _crawl_over_directory(dir_path: str) -> dict:
    files_content = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_content[file_path] = _read_lines_from_file(file_path)
    return files_content


def _read_lines_from_file(file_name: str) -> List[str]:
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f]
    return lines
