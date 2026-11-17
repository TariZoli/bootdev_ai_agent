import os
from functions.config import MAX_CHAR

def get_file_content(working_directory: str, file_path: str) -> str:
    
    working_dir_abs = os.path.abspath(working_directory)
    file_path = os.path.normpath(
        os.path.join(working_dir_abs, file_path)
    )

    if os.path.commonpath([working_dir_abs, file_path]) != working_dir_abs:
        return (
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        )

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

   

    
    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHAR)
                
        if f.read(MAX_CHAR+1):
            file_content_string +=  f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
        return file_content_string

    if file_content_string == '':
        return 'Error: canot run command'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the text content of a file, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to read, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}