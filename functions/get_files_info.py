import os
import google.generativeai as genai
from google.generativeai import types


def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)
    working_dir_abs = os.path.abspath(working_directory)
    target_path_abs = os.path.abspath(full_path)
    if not target_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path_abs):
        return f'Error: "{directory}" is not a directory'

    dir_content_str = ""

    try:
        for obj in os.listdir(full_path):
            full_obj_path = os.path.join(full_path, obj)
            file_size = os.path.getsize(full_obj_path)
            is_dir = os.path.isdir(full_obj_path)
            dir_content_str += f'- {obj}: file_size={file_size} bytes, is_dir={is_dir}\n'
    except Exception as e:
        error_message = str(e)
        return f'Error: {error_message}'

    return dir_content_str

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "directory": {
                "type": "STRING",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            },
        },
        "required": []
    },
)
