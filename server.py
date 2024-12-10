import os
import hashlib
from fastapi import FastAPI, File, UploadFile
from typing import List
from collections import Counter

# Directory to store files
UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dictionary to store file hashes (In production, this would ideally be a database)
file_hashes = {}

app = FastAPI()


# Helper function to get file hash (SHA256)
def get_file_hash(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to avoid loading large files completely into memory
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# Helper function to count words
def count_words(file_path):
    with open(file_path, "r") as f:
        text = f.read()
        words = text.split()
        return len(words), words


# 1. Add files to the store with duplicate check
@app.post("/files/add")
async def add_files(files: List[UploadFile] = File(...)):
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Check if the file already exists in the directory
        if os.path.exists(file_path):
            return {"message": f"File {file.filename} already exists."}

        # Check if the file content (hash) already exists in the store
        file_content = await file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()

        # If the file with the same content exists, skip the upload
        if file_hash in file_hashes:
            return {"message": f"File with the same content as {file.filename} already exists."}

        # Save the file
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Store the hash of the file for future comparison
        file_hashes[file_hash] = file.filename

    return {"message": "Files uploaded successfully"}


# 2. List files in the store
@app.get("/files")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}


# 3. Remove a file
@app.delete("/files/{filename}")
async def remove_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File {filename} removed successfully."}
    return {"message": f"File {filename} not found."}


# 4. Update file content
@app.put("/files/{filename}")
async def update_file(filename: str, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Check if file exists
    if not os.path.exists(file_path):
        return {"message": f"File {filename} does not exist."}

    # Write new content
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": f"File {filename} updated successfully."}


# 5. Word count for all files
@app.get("/files/wc")
async def word_count():
    total_words = 0
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        word_count, _ = count_words(file_path)
        total_words += word_count
    return {"total_words": total_words}


# 6. Get most frequent words
@app.get("/files/freq-words")
async def frequent_words(limit: int = 10, order: str = 'dsc'):
    word_counter = Counter()
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        _, words = count_words(file_path)
        word_counter.update(words)

    sorted_words = word_counter.most_common() if order == 'dsc' else word_counter.most_common()[::-1]
    return {"frequent_words": sorted_words[:limit]}
