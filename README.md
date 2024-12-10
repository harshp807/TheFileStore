

# File Store CLI

A command-line interface (CLI) to manage files on a server, with functionalities to add, list, remove, update files, retrieve word counts, and fetch frequent words across all files. Built with FastAPI and Python.

## Prerequisites

- Python 3.x
- FastAPI
- Requests library

You can install the necessary libraries using:
```bash
pip install fastapi requests
```

## Setup and Running the Server

1. Clone the repository and navigate to the project directory.
2. Start the FastAPI server by running:
   ```bash
   uvicorn server:app --reload
   ```

## CLI Usage

This CLI interacts with the FastAPI server to manage files. You can run the CLI commands to perform various file operations.

### Commands

#### `add`
Add one or more files to the server.

**Usage**:
```bash
python client.py add <file1> <file2> ...
```

Example:
```bash
python client.py add file1.txt file2.txt
```

#### `ls`
List all files currently stored on the server.

**Usage**:
```bash
python client.py ls
```

#### `rm`
Remove a specific file from the server.

**Usage**:
```bash
python client.py rm <filename>
```

Example:
```bash
python client.py rm file1.txt
```

#### `update`
Update an existing file on the server with a new file.

**Usage**:
```bash
python client.py update <filename> <new_file>
```

Example:
```bash
python client.py update file1.txt new_file.txt
```

#### `wc`
Get the total word count for all files stored on the server.

**Usage**:
```bash
python client.py wc
```

#### `freq-words`
Get the most or least frequent words across all files stored on the server. You can specify the number of words to return with `--limit` (or `-n`), and control the sorting order with `--order` (either `asc` or `dsc`).

**Usage**:
```bash
python client.py freq-words --limit <number> --order <asc|dsc>
```

Example:
```bash
python client.py freq-words --limit 10 --order dsc
```

### Parameters for `freq-words`

- `--limit, -n`: Limit the number of words returned (default is 10).
- `--order`: Sort the words either in ascending (`asc`) or descending (`dsc`) order of frequency.

---

This `README.md` file now reflects the updated functionality of the CLI commands, including adding support for word count and frequent words operations. Let me know if you'd like to add or modify anything else!
