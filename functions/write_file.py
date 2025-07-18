import os
import google.generativeai as genai
from google.generativeai import types


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    working_dir_abs = os.path.abspath(working_directory)
    target_path_abs = os.path.abspath(full_path)

    try:
        if not target_path_abs.startswith(working_dir_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dir_name = os.path.dirname(target_path_abs)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(target_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        error_message = str(e)
        return f'Error: {error_message}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates/overwrites listed file with provided content, constrained to the working directory.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "file_path": {
                "type": "STRING",
                "description": "File to which the content is written, constrained to the working directory."
            },
            "content": {
                "type": "STRING",
                "description": "Content written to file, constrained to the working directory."
            }
        },
        "required": []
    },
)
