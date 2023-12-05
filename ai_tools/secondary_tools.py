import json
import subprocess

def create_file(fileName, fileContent):
    try:
        with open(fileName, 'w') as file:
            file.write(fileContent)
        return f"File '{fileName}' created successfully."
    except IOError as e:
        return f"Error creating file: {e}"

def execute_file(fileName):
    """
    Executes a Python file.
    :param filename: Name of the file to execute.
    """
    try:
        result = subprocess.run(['python', fileName], capture_output=True, text=True, check=True)
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