

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
