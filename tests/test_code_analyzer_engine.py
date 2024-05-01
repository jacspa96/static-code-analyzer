import unittest
from code_analyzer_engine import CodeAnalyzerEngine


TEST_CODE_FILE_NAME = "test_code_file.txt"


class TestCodeAnalyzer(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.code_analyzer_to_test = CodeAnalyzerEngine(TEST_CODE_FILE_NAME)

    def test_check_line_length(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 3: S001 Too long",
                           f"{TEST_CODE_FILE_NAME}: Line 6: S001 Too long"]

        # when
        actual_errors = self.code_analyzer_to_test.check_line_length(TEST_CODE_FILE_NAME)

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_check_indentation(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 12: S002 Indentation is not a multiple of four",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S002 Indentation is not a multiple of four",]

        # when
        actual_errors = self.code_analyzer_to_test.check_indentation(TEST_CODE_FILE_NAME)

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_check_comments(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 1: S004 At least two spaces required before inline comments",
                           f"{TEST_CODE_FILE_NAME}: Line 2: S003 Unnecessary semicolon",
                           f"{TEST_CODE_FILE_NAME}: Line 3: S003 Unnecessary semicolon",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S003 Unnecessary semicolon",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S004 At least two spaces required before inline comments",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S005 TODO found"]

        # when
        actual_errors = self.code_analyzer_to_test.check_comments(TEST_CODE_FILE_NAME)

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_blank_lines(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 11: S006 More than two blank lines used before this line"]

        # when
        actual_errors = self.code_analyzer_to_test.check_blank_lines(TEST_CODE_FILE_NAME)

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_check_spaces_after_declaration(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 15: S007 Too many spaces after 'class'"]

        # when
        actual_errors = self.code_analyzer_to_test.check_spaces_after_declaration(TEST_CODE_FILE_NAME)

        # then
        self.assertListEqual(expected_errors, actual_errors)


    def test_check_naming(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 18: S008 Class name 'user' should use CamelCase",
                           f"{TEST_CODE_FILE_NAME}: Line 32: S010 Argument name 'S' should be snake_case",
                           f"{TEST_CODE_FILE_NAME}: Line 32: S012 Default argument value is mutable",
                           f"{TEST_CODE_FILE_NAME}: Line 37: S011 Variable 'badVar' should be snake_case",
                           f"{TEST_CODE_FILE_NAME}: Line 29: S009 Function name 'Print2' should use snake_case",
                           f"{TEST_CODE_FILE_NAME}: Line 33: S011 Variable 'VARIABLE' should be snake_case"]

        # when
        actual_errors = self.code_analyzer_to_test.check_naming(TEST_CODE_FILE_NAME)

        # then
        self.assertListEqual(expected_errors, actual_errors)

    def test_analyze_code(self):
        # given
        expected_errors = [f"{TEST_CODE_FILE_NAME}: Line 1: S004 At least two spaces required before inline comments",
                           f"{TEST_CODE_FILE_NAME}: Line 2: S003 Unnecessary semicolon",
                           f"{TEST_CODE_FILE_NAME}: Line 3: S001 Too long",
                           f"{TEST_CODE_FILE_NAME}: Line 3: S003 Unnecessary semicolon",
                           f"{TEST_CODE_FILE_NAME}: Line 6: S001 Too long",
                           f"{TEST_CODE_FILE_NAME}: Line 11: S006 More than two blank lines used before this line",
                           f"{TEST_CODE_FILE_NAME}: Line 12: S002 Indentation is not a multiple of four",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S002 Indentation is not a multiple of four",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S003 Unnecessary semicolon",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S004 At least two spaces required before inline comments",
                           f"{TEST_CODE_FILE_NAME}: Line 13: S005 TODO found",
                           f"{TEST_CODE_FILE_NAME}: Line 15: S007 Too many spaces after 'class'",
                           f"{TEST_CODE_FILE_NAME}: Line 18: S008 Class name 'user' should use CamelCase",
                           f"{TEST_CODE_FILE_NAME}: Line 29: S009 Function name 'Print2' should use snake_case",
                           f"{TEST_CODE_FILE_NAME}: Line 32: S010 Argument name 'S' should be snake_case",
                           f"{TEST_CODE_FILE_NAME}: Line 32: S012 Default argument value is mutable",
                           f"{TEST_CODE_FILE_NAME}: Line 33: S011 Variable 'VARIABLE' should be snake_case",
                           f"{TEST_CODE_FILE_NAME}: Line 37: S011 Variable 'badVar' should be snake_case"]

        # when
        actual_errors = self.code_analyzer_to_test.analyze_code()

        # then
        self.assertListEqual(expected_errors, actual_errors)


if __name__ == '__main__':
    unittest.main()
