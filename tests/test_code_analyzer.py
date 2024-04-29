import unittest
from code_analyzer import CodeAnalyzer


TEST_CODE_FILE_NAME = "test_code_file.txt"


class TestCodeAnalyzer(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.code_analyzer_to_test = CodeAnalyzer(TEST_CODE_FILE_NAME)

    def test_check_line_length(self):
        # given
        expected_errors = ["Line 3: S001 Too long",
                           "Line 6: S001 Too long"]

        # when
        actual_errors = self.code_analyzer_to_test.check_line_length()

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_check_indentation(self):
        # given
        expected_errors = ["Line 12: S002 Indentation is not a multiple of four"]

        # when
        actual_errors = self.code_analyzer_to_test.check_indentation()

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_check_comments(self):
        # given
        expected_errors = ["Line 1: S004 At least two spaces required before inline comments",
                           "Line 2: S003 Unnecessary semicolon",
                           "Line 3: S003 Unnecessary semicolon",
                           "Line 13: S003 Unnecessary semicolon",
                           "Line 13: S004 At least two spaces required before inline comments",
                           "Line 13: S005 TODO found"]

        # when
        actual_errors = self.code_analyzer_to_test.check_comments()

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_blank_lines(self):
        # given
        expected_errors = ["Line 11: S006 More than two blank lines used before this line"]

        # when
        actual_errors = self.code_analyzer_to_test.check_blank_lines()

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_analyze_code(self):
        # given
        expected_errors = ["Line 1: S004 At least two spaces required before inline comments",
                           "Line 2: S003 Unnecessary semicolon",
                           "Line 3: S001 Too long",
                           "Line 3: S003 Unnecessary semicolon",
                           "Line 6: S001 Too long",
                           "Line 11: S006 More than two blank lines used before this line",
                           "Line 12: S002 Indentation is not a multiple of four",
                           "Line 13: S003 Unnecessary semicolon",
                           "Line 13: S004 At least two spaces required before inline comments",
                           "Line 13: S005 TODO found"]

        # when
        actual_errors = self.code_analyzer_to_test.analyze_code()

        # then
        self.assertListEqual(expected_errors, actual_errors)


if __name__ == '__main__':
    unittest.main()
