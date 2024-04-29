import unittest
from code_analyzer import analyze_code


class TestCodeAnalyzer(unittest.TestCase):

    def test_line_length(self):
        # given
        file_name = "long_lines.txt"
        expected_errors = ["Line 3: S001 Too long",
                           "Line 5: S001 Too long"]

        # when
        actual_errors = analyze_code(file_name)

        # then
        self.assertListEqual(expected_errors, actual_errors)


if __name__ == '__main__':
    unittest.main()
