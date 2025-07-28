import os
import sys
import json
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
from google.protobuf.json_format import MessageToDict


def cont_to_dict(content):
    parts_as_dicts = []
    for part in content.parts:
        if hasattr(part, "function_call") and part.function_call is not None:
            # Make a dict representing the function_call
            parts_as_dicts.append({
                "function_call": {
                    "name": part.function_call.name,
                    "args": part.function_call.args
                }
            })
        elif hasattr(part, "text") and part.text is not None:
            # Make a dict for the text
            parts_as_dicts.append({"text": part.text})
        # You could handle more types here as needed

    return {
        "role": content.role,
        "parts": parts_as_dicts
    }

def generate_content(messages, verbose=False, model=None):
    for i in range(0, 20):
        try:
            response = model.generate_content(messages)

            function_calls_found = False
            for candidate in response.candidates:
                messages.append(candidate.content)

                # Only process parts that have valid function calls
                valid_function_calls = []
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call.name:
                        valid_function_calls.append(part.function_call)

                # Execute valid function calls
                for function_call in valid_function_calls:
                    function_calls_found = True
                    if verbose:
                        print(f" - Calling function: {function_call.name}")

                    function_call_result = call_function(function_call, verbose)
                    messages.append(function_call_result)

            if not function_calls_found:
                print(response.text)
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    return response

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent with access to file system tools.

    When a user asks about code or files, you should:
    1. First use get_files_info to explore the directory structure
    2. Use get_file_content to read relevant files
    3. Use run_python_file to execute code if needed
    4. Use write_file to create or modify files if requested

    You have access to these functions:
    - get_files_info: List files and directories
    - get_file_content: Read file contents  
    - run_python_file: Execute Python files with optional arguments
    - write_file: Write or overwrite files

    Always start by exploring the file system to understand the codebase before answering questions.
    All paths should be relative to the working directory.
    """

    user_prompt = ''
    if len(sys.argv) > 1:
        user_prompt += sys.argv[1]
    else:
        print("No prompts (arguments) provided. Exiting with Code 1.")
        sys.exit(1)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    model = genai.GenerativeModel(
        'gemini-2.0-flash-001',
        tools=[available_functions],
        system_instruction=system_prompt
    )

    messages = [genai.protos.Content(role="user", parts=[genai.protos.Part(text=user_prompt)])]
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    response = generate_content(messages, verbose, model)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print()



if __name__ == "__main__":
    main()
