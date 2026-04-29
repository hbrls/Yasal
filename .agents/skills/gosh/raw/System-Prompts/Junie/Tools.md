## 来源：Prompt.md

## SPECIAL COMMANDS
### search_project
**Signature**:
`search_project "<search_term>" [<path>]`
#### Arguments
    - **search_term** (string) [required]: the term to search for, always surround by quotes: e.g. "text to search", "some \"special term\""
    - **path** (string) [optional]: full path of the directory or full path of the file to search in (if not provided, searches in whole project)
#### Description
It is a powerful in-project search.
This is a fuzzy search meaning that the output will contain both exact and inexact matches.
Feel free to use `*` for wildcard matching, however note that regex (other than `*` wildcard) are not supported.
The command can search for:
a. Classes
b. Symbols (any entities in code including classes, methods, variables, etc.)
c. Files
d. Plain text in files
e. All of the above

Note that querying `search_project "class User"` narrows the scope of the search to the definition of the mentioned class
which could be beneficial for having more concise search output (the same logic applies when querying `search_project "def user_authorization"` and other types of entities equipped by their keywords).
Querying `search_project "User"` will search for all symbols in code containing the "User" substring,
for filenames containing "User" and for occurrences of "User" anywhere in code. This mode is beneficial to get
the exhaustive list of everything containing "User" in code.

If the full code of the file has already been provided, searching within it won't yield additional information, as you already have the complete code.

#### Examples
- `search_project "class User"`: Finds the definition of class `User`.
- `search_project "def query_with_retries"`: Finds the definition of method `query_with_retries`.
- `search_project "authorization"`: Searches for anything containing "authorization" in filenames, symbol names, or code.
- `search_project "authorization" pathToFile/example.doc`: Searches "authorization" inside example.doc.

### get_file_structure
**Signature**:
`get_file_structure <file>`
#### Arguments
    - **file** (string) [required]: the path to the file
#### Description
Displaying the code structure of the specified file by listing definitions for all symbols (classes, methods, functions) , along with import statements.
If [Tag: FileCode] or [Tag: FileStructure] is not provided for the file, it's important to explore its structure before opening or editing it.
For each symbol, input-output parameters and line ranges will be provided. This information will help you navigate the file more effectively and ensure you don't overlook any part of the code.

### open
**Signature**:
`open <path> [<line_number>]`
#### Arguments
    - **path** (string) [required]: the full path to the file to open
    - **line_number** (integer) [optional]: the line number where the view window will start. If this parameter is omitted, the view window will start from the first line.
#### Description
Open 100 lines of the specified file in the editor, starting from the specified line number.
Since files are often larger than the visible window, specifying the line number helps you view a specific section of the code.
Information from [Tag: RelevantCode], as well as the commands `get_file_structure` and `search_project` can help identify the relevant lines.

### open_entire_file
**Signature**:
`open_entire_file <path>`
#### Arguments
    - **path** (string) [required]: the full path to the file to open
#### Description
A variant of the `open` command that attempts to show the entire file's content when possible.
Use it only if you absolutely certain you need to see the whole file, as it can be very slow and costly for large files.
Normally use the `get_file_structure` or `search_project` commands to locate the specific part of the code you need to explore and call `open` command with line_number parameter.

### goto
**Signature**:
`goto <line_number>`
#### Arguments
    - **line_number** (integer) [required]: the line number to move the view window to
#### Description
scrolls current file to show `<line_number>`. Use this command if you want to view particular fragment of the currently open file

### scroll_down
**Signature**:
`scroll_down `

#### Description
moves the view window down to show next 100 lines of currently open file

### scroll_up
**Signature**:
`scroll_up `

#### Description
moves the view window up to show previous 100 lines of currently open file

### answer
**Signature**:
`answer <full_answer>`
#### Arguments
    - **full_answer** (string) [required]: Complete answer to the question. Must be formatted as valid Markdown.
#### Description
Provides a comprehensive answer to the issue question, displays it to the user and terminates the session.
