import argparse
import requests
import os

BASE_URL = "http://127.0.0.1:8000"  # URL of your FastAPI server


# Helper function to add files
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


# Helper function to list files
def list_files():
    response = requests.get(f"{BASE_URL}/files")
    print(response.json())


# Helper function to remove files
def remove_file(filename):
    response = requests.delete(f"{BASE_URL}/files/{filename}")
    print(response.json())


# Helper function to update files
def update_file(filename, new_file):
    files = {'file': open(new_file, 'rb')}
    response = requests.put(f"{BASE_URL}/files/{filename}", files=files)
    print(response.json())
    files['file'].close()


# Helper function to get word count
def word_count():
    response = requests.get(f"{BASE_URL}/files/wc")
    print(response.json())


# Helper function to get most frequent or least frequent words
def frequent_words(limit=10, order="dsc"):
    response = requests.get(f"{BASE_URL}/files/freq-words", params={"limit": limit, "order": order})
    print(response.json())


# Main entry for the command line interface
def main():
    parser = argparse.ArgumentParser(description="File Store CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add files command
    add_parser = subparsers.add_parser("add", help="Add files to the store")
    add_parser.add_argument("files", nargs='+', help="List of files to add")

    # List files command
    list_parser = subparsers.add_parser("ls", help="List files in the store")

    # Remove files command
    remove_parser = subparsers.add_parser("rm", help="Remove a file from the store")
    remove_parser.add_argument("filename", help="Filename to remove")

    # Update files command
    update_parser = subparsers.add_parser("update", help="Update file in the store")
    update_parser.add_argument("filename", help="Filename to update")
    update_parser.add_argument("new_file", help="New file to upload")

    # Word count command
    wc_parser = subparsers.add_parser("wc", help="Get word count for all files in the store")

    # Frequent words command
    freq_parser = subparsers.add_parser("freq-words", help="Get most frequent or least frequent words in the store")
    freq_parser.add_argument("--limit", "-n", type=int, default=10, help="Limit the number of words")
    freq_parser.add_argument("--order", choices=["asc", "dsc"], default="dsc", help="Order of the words")

    args = parser.parse_args()

    if args.command == "add":
        add_files(args.files)
    elif args.command == "ls":
        list_files()
    elif args.command == "rm":
        remove_file(args.filename)
    elif args.command == "update":
        update_file(args.filename, args.new_file)
    elif args.command == "wc":
        word_count()
    elif args.command == "freq-words":
        frequent_words(args.limit, args.order)


if __name__ == "__main__":
    main()
