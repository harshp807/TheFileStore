

```markdown
# File Store Service

This project implements a file store service that allows users to upload, list, remove, and update files through a RESTful API. The server-side application uses **FastAPI**, and the client-side application is a simple **CLI** that interacts with the server via HTTP requests.

## Features
- Add files to the server.
- List all files on the server.
- Remove files from the server.
- Update files already stored on the server.
- Perform word count and frequency analysis on all stored files.
- Handle duplicate files using SHA256 hashing.

## Installation

### Server-Side (FastAPI)

To set up the server, you'll need to install the required dependencies:

```bash
pip install fastapi uvicorn python-multipart
```

Create a directory to store the uploaded files:

```bash
mkdir uploaded_files
```

### Server Implementation (`server.py`)

The FastAPI server exposes various endpoints for file operations:

1. **Add files** (`/files/add`): Upload multiple files.
2. **List files** (`/files`): List all files stored on the server.
3. **Remove file** (`/files/{filename}`): Delete a specific file.
4. **Update file** (`/files/{filename}`): Replace an existing file's content.
5. **Word count** (`/files/wc`): Count the total number of words in all files.
6. **Frequent words** (`/files/freq-words`): Get the most frequent words across all files.

Example server code:

```python
from fastapi import FastAPI, File, UploadFile
from typing import List
import os
from collections import Counter
import hashlib

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

file_hashes = {}

app = FastAPI()

def get_file_hash(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.post("/files/add")
async def add_files(files: List[UploadFile] = File(...)):
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        if os.path.exists(file_path):
            return {"message": f"File {file.filename} already exists."}
        
        file_content = await file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        if file_hash in file_hashes:
            return {"message": f"File with the same content as {file.filename} already exists."}
        
        with open(file_path, "wb") as f:
            f.write(file_content)

        file_hashes[file_hash] = file.filename

    return {"message": "Files uploaded successfully"}
```

To run the server:

```bash
uvicorn server:app --reload
```

---

### Client-Side (CLI)

The client interacts with the server using the **requests** library. You can install it using:

```bash
pip install requests
```

### Client Implementation (`client.py`)

The client provides several commands to interact with the server:

- **Add files** (`python client.py add file1.txt file2.txt`)
- **List files** (`python client.py ls`)
- **Remove files** (`python client.py rm file1.txt`)
- **Update files** (`python client.py update file1.txt new_file.txt`)

Example client code:

```python
import argparse
import requests
import os

BASE_URL = "http://127.0.0.1:8000"

def add_files(files):
    files_to_send = []
    for file in files:
        if os.path.exists(file):
            files_to_send.append(('files', open(file, 'rb')))
        else:
            print(f"File {file} does not exist.")
            return

    response = requests.post(f"{BASE_URL}/files/add", files=files_to_send)
    print(response.json())
    for f in files_to_send:
        f[1].close()

def list_files():
    response = requests.get(f"{BASE_URL}/files")
    print(response.json())

def remove_file(filename):
    response = requests.delete(f"{BASE_URL}/files/{filename}")
    print(response.json())

def update_file(filename, new_file):
    files = {'file': open(new_file, 'rb')}
    response = requests.put(f"{BASE_URL}/files/{filename}", files=files)
    print(response.json())
    files['file'].close()

def main():
    parser = argparse.ArgumentParser(description="File Store CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add files to the store")
    add_parser.add_argument("files", nargs='+', help="List of files to add")

    list_parser = subparsers.add_parser("ls", help="List files in the store")

    remove_parser = subparsers.add_parser("rm", help="Remove a file from the store")
    remove_parser.add_argument("filename", help="Filename to remove")

    update_parser = subparsers.add_parser("update", help="Update file in the store")
    update_parser.add_argument("filename", help="Filename to update")
    update_parser.add_argument("new_file", help="New file to upload")

    args = parser.parse_args()

    if args.command == "add":
        add_files(args.files)
    elif args.command == "ls":
        list_files()
    elif args.command == "rm":
        remove_file(args.filename)
    elif args.command == "update":
        update_file(args.filename, args.new_file)

if __name__ == "__main__":
    main()
```

---

## Testing the Service

Once the server is running, you can use the client to perform various operations:

1. **Add files**:

```bash
python client.py add file1.txt file2.txt
```

2. **List files**:

```bash
python client.py ls
```

3. **Remove a file**:

```bash
python client.py rm file1.txt
```

4. **Update a file**:

```bash
python client.py update file1.txt new_file.txt
```

### Duplicate File Handling

To prevent the upload of duplicate files (based on their content), the server calculates a **SHA256** hash for each file. If a file with the same hash exists, the upload is skipped.

The client automatically benefits from this feature since it interacts with the server that handles duplicates.

---

## Conclusion

This project provides a simple yet efficient file store service with additional features such as word count analysis, frequent word identification, and duplicate file handling using hashing. It demonstrates a practical usage of **FastAPI** for server-side file management and a **Python CLI** for easy client interaction.
```

This structure organizes the server and client-side instructions, along with testing information and feature explanations. It includes code snippets for both sides and clear installation instructions for setting up the project.
