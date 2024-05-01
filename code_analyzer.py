import sys
from code_analyzer_engine import CodeAnalyzerEngine



def parse_args() -> str:
    args = sys.argv
    if len(args) != 2:
        raise ValueError(f"Expected exactly 1 command line argument, received {len(args) - 1}")
    file_name = args[1]
    return file_name


def main():
    file_name = parse_args()
    code_analyzer = CodeAnalyzerEngine(file_name)
    errors = code_analyzer.analyze_code()
    print(*errors, sep="\n")


if __name__ == '__main__':
    main()
