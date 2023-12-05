import json
import subprocess
import os

def create_file(fileName, fileContent):
    sandbox_dir = "sandbox"
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

def execute_file(fileName):
    sandbox_dir = "sandbox"
    # Adjust the file path to include the sandbox directory
    filePath = os.path.join(sandbox_dir, fileName)

    try:
        result = subprocess.run(['python3', filePath], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing file: {e.output}"


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
}]