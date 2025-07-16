import os
import sys
import json
from functions.get_files_info import schema_get_files_info
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
                # Try multiple ways to access the args
                args = part.function_call.args

                # Method 1: Try treating it as a dict
                try:
                    args_dict = dict(args)
                    print(f"Calling function: {part.function_call.name}({args_dict})")
                    continue
                except:
                    pass

                # Method 2: Try accessing specific keys
                try:
                    args_dict = {}
                    for key in ['directory']:
                        if key in args:
                            args_dict[key] = args[key]
                    print(f"Calling function: {part.function_call.name}({args_dict})")
                    continue
                except:
                    pass

                # Method 3: Debug - see what methods/attributes are available
                print(f"Args type: {type(args)}")
                print(f"Args dir: {[attr for attr in dir(args) if not attr.startswith('_')]}")
                print(f"Calling function: {part.function_call.name}({args})")

    if not function_calls_found:
        print(response.text)


if __name__ == "__main__":
    main()
