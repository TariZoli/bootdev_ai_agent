import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    
    working_dir_abs = os.path.abspath(working_directory)
    file_path = os.path.normpath(
        os.path.join(working_dir_abs, file_path)
    )

    if os.path.commonpath([working_dir_abs, file_path]) != working_dir_abs:
        return (
            f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        )

    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    parent_dir  = os.path.dirname(file_path)
    os.makedirs(name=parent_dir, exist_ok=True)

    try:
        with open(file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except:
        return 'Error:proccess cannot complet'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file, creating it or overwriting it if it exists, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The full text content to write to the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}