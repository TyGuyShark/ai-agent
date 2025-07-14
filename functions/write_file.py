import os


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
