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

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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

    response = model.generate_content(user_prompt)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print()

    # Check if there are function calls in the response
    function_calls_found = False
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if hasattr(part, 'function_call'):
                function_calls_found = True

                # Check if verbose is enabled
                verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

                # Call the function
                function_call_result = call_function(part.function_call, verbose)

                # Handle the result according to the lesson requirements
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function call failed to return a response")

                if verbose:
                    result_obj = function_call_result.parts[0].function_response.response
                    if "result" in result_obj:
                        print(f"-> {result_obj['result']}")
                    elif "error" in result_obj:
                        print(f"-> ERROR: {result_obj['error']}")
                    else:
                        print(f"-> Unknown response: {result_obj}")
    if not function_calls_found:
        print(response.text)


if __name__ == "__main__":
    main()
