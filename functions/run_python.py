import os
import fnmatch
import subprocess

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    working_dir_abs = os.path.abspath(working_directory)
    target_path_abs = os.path.abspath(full_path)

    try:
        if not target_path_abs.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_path_abs):
            return f'Error: File "{file_path}" not found.'
        if not fnmatch.fnmatch(file_path, '*.py'):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            ['python3', target_path_abs],
            capture_output=True,
            timeout=30,
            text=True,
            cwd=working_dir_abs
        )
        if not result.stdout and not result.stderr:
            return 'No output produced.'

        output = ''
        output += f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\n'
        if not result.returncode != 0:
            output += f'Process exited with code {result.returncode}\n'
        return output

    except Exception as e:
        error_message = str(e)
        return f'Error: executing Python file: {error_message}'
