import json
import subprocess
import os
import shutil
from flask import jsonify

def create_file(fileName, fileContent, user_id):
    sandbox_dir = os.path.join("sandbox", user_id)  # Construct the directory path with user_id
    # Ensure the sandbox directory exists
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    # Adjust the file path to include the sandbox directory
    filePath = os.path.join(sandbox_dir, fileName)

    try:
        with open(filePath, 'w') as file:
            file.write(fileContent)
        return f"File '{filePath}' created successfully."
    except IOError as e:
        return f"Error creating file: {e}"
   

def execute_file(fileName, user_id):
    sandbox_dir =  os.path.join("sandbox", user_id)
    # Adjust the file path to include the sandbox directory
    filePath = os.path.join(sandbox_dir, fileName)

    try:
        result = subprocess.run(['python3', filePath], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing file: {e.output}"

def move_files(file_moves, user_id):
    sandbox_dir =  os.path.join("sandbox", user_id)
    results = []

    # Ensure the sandbox directory exists
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    for file_move in file_moves:
        file_name = file_move["fileName"]
        destination_subdir = file_move["destination"]

        # Ensure the target subdirectory exists
        target_dir = os.path.join(sandbox_dir, destination_subdir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        source_path = os.path.join(sandbox_dir, file_name)
        if os.path.exists(source_path):
            destination_path = os.path.join(target_dir, file_name)
            try:
                shutil.move(source_path, destination_path)
                results.append(f"Moved '{source_path}' to '{destination_path}'")
            except IOError as e:
                results.append(f"Error moving file '{file_name}': {e}")
        else:
            results.append(f"File '{file_name}' not found in '{sandbox_dir}'")

    return results

# Example usage:
# file_moves = [
#     {"fileName": "file1.txt", "destination": "tested-working"},
#     {"fileName": "file2.txt", "destination": "tested-unworking"}
# ]
# results = move_files(file_moves)
# for result in results:
#     print(result)


tools_lite = [{
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "saves to files locally",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": "give the file a name eg: filename.py"
                },
                "fileContent": {
                    "type": "string",
                    "description": "write here the content for the file"
                },
            },
            "required": ["fileName", "fileCOntent"]
        }}}, {
    "type": "function",
    "function": {
        "name": "execute_file",
        "description": "for executing py scripts",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": "provide the name of the file you want to execute: eg: fileName.py"
                }
            },
            "required": ["fileName"]
        }
    }
},{
    "type": "function",
    "function": {
        "name": "move_files",
        "description": "moves files to specified subdirectories based on individual status",
        "parameters": {
            "type": "object",
            "properties": {
                "fileMoves": {
                    "type": "array",
                    "description": "list of objects containing file names and their respective destinations",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fileName": {
                                "type": "string",
                                "description": "name of the file to be moved"
                            },
                            "destination": {
                                "type": "string",
                                "enum": ["tested-working", "tested-unworking"],
                                "description": "destination subdirectory for the file ('tested-working' or 'tested-unworking')"
                            }
                        },
                        "required": ["fileName", "destination"]
                    }
                }
            },
            "required": ["fileMoves"]
        }
    }
}]