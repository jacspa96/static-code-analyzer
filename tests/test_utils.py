import unittest
from utils import extract_line_number, _crawl_over_directory, _read_lines_from_file


class TestUtils(unittest.TestCase):

    def test_extract_line_number(self):
        # given
        message = "C:\\Users\\test_user\\file.py: Line 1: S000 Some error"
        expected_line_number = 1

        # when
        actual_line_number = extract_line_number(message)

        # then
        self.assertEqual(expected_line_number, actual_line_number)

    def test_crawl_over_directory(self):
        # given
        expected_files = ["./crawling_test\\test_file_1",
                          "./crawling_test\\nested_dir\\test_file_2"]
        start_path = "./crawling_test"

        # when
        actual_files = list(_crawl_over_directory(start_path).keys())

        # then
        self.assertListEqual(expected_files, actual_files)

    def test_read_lines_from_file(self):
        expected_lines = ["print('What\\'s your name?') # reading an input",
                          "name = input();",
                          "print(f'Hello, {name}');  # here is an obvious comment: this prints a greeting with a name",
                          "",
                          "",
                          "very_big_number = 11_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000",
                          "print(very_big_number)",
                          "",
                          "",
                          "",
                          "def some_fun():",
                          "     print('NO TODO HERE;;')",
                          "    pass; # Todo something"]

        actual_lines = _read_lines_from_file("test_code_file.txt")

        self.assertListEqual(expected_lines, actual_lines)


if __name__ == '__main__':
    unittest.main()
