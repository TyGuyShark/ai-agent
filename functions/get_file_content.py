import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    working_dir_abs = os.path.abspath(working_directory)
    target_path_abs = os.path.abspath(full_path)

    try:
        if not target_path_abs.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            size_check = f.read(1)
            if size_check != "":
                file_content_string += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

    except Exception as e:
        error_message = str(e)
        return f'Error: {error_message}'
