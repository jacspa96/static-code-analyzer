import os
import ast
from typing import List


MESSAGE_PARTS_SEPARATOR = ": "
LINE_INFO_POSITION = 1
LINE_NUMBER_POSITION = 1


def extract_line_number(message: str) -> int:
    line_info = message.split(MESSAGE_PARTS_SEPARATOR)[LINE_INFO_POSITION]
    line_number = int(line_info.split(" ")[LINE_NUMBER_POSITION])
    return line_number


def extract_name_from_declaration(declaration: str) -> str:
    name = declaration.split()[1]  # get rid of "class" or "def" keyword at position 0
    name = name.replace(":", "").rstrip()
    name = name.split("(")[0]  # get rid of parent class or function parameters
    return name


def read_contents_of_all_files(path: str) -> dict:
    if os.path.isfile(path):
        return {path: _read_lines_from_file(path)}
    else:
        return _crawl_over_directory_and_read_lines(path)


def read_code_trees_of_all_files(path: str) -> dict:
    if os.path.isfile(path):
        return {path: _read_code_tree_from_file(path)}
    else:
        return _crawl_over_directory_and_read_trees(path)


def _crawl_over_directory_and_read_lines(dir_path: str) -> dict:
    files_content = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_content[file_path] = _read_lines_from_file(file_path)
    return files_content


def _crawl_over_directory_and_read_trees(dir_path: str) -> dict:
    files_content = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_content[file_path] = _read_code_tree_from_file(file_path)
    return files_content


def _read_lines_from_file(file_name: str) -> List[str]:
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f]
    return lines


def _read_code_tree_from_file(file_name: str) -> ast.Module:
    with open(file_name, "r") as f:
        tree = ast.parse(f.read())
    return tree
