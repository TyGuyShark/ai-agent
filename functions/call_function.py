import os
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.write_file import write_file
import google.generativeai as genai

def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    args = dict(function_call_part.args) if function_call_part.args else {}
    args["working_directory"] = "./calculator"
    available_functions = {
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
        "write_file": write_file
    }

    if not function_call_part.name in available_functions:
        return genai.protos.Content( # Use genai.protos.Content for the overall Content object
             role="tool",
             parts=[
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse( # Pass a FunctionResponse object
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                )
            ],
        )

    function_result = available_functions[function_call_part.name](**args)
    return genai.protos.Content( # Use genai.protos.Content for the overall Content object
        role="tool",
        parts=[
            genai.protos.Part( # Create a Part object
                function_response=genai.protos.FunctionResponse( # Pass a FunctionResponse object
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            )
        ],
    )
