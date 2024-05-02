# Static Code Analyzer

This repo contains my implementation of project Static Code Analyzer from JetBrains Academy (https://hyperskill.org/projects/127).

### Usage

This program check the python code in terms of its style, adhering to naming conventions, following proper indentation etc. 

To run the program type ```python code_analyzer.py {path_to_code}```, where ```{path_to_code}``` is either a path to a specific file with code or to the directory with code files. 
In the latter case, program will crawl over the directory and analyze all the files there.

Program prints identified issues in the following message format:  
```{file_name}: {line_number}: {issue_code} {message}```

Following issues with the code are checked, with their corresponding ```{issue_code}```:

* ```S001``` - Too long line
* ```S002``` - Indentation is not a multiple of four
* ```S003``` - Unnecessary semicolon at the end of the line
* ```S004``` - There should be at least two spaces before inline comments
* ```S005``` - TODO found
* ```S006``` - More than two blank lines used before the line
* ```S007``` - Too many spaces after class or function declaration
* ```S008``` - Class name should follow camel case
* ```S009``` - Function name should follow snake case
* ```S010``` - Function argument name should follow snake case
* ```S011``` - Variable name should follow snake case
* ```S012``` - Default argument value in function is mutable

For last 5 checks Abstract Syntax Tree is used (using ```ast``` module https://docs.python.org/3/library/ast.html).
