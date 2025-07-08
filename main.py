import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    print(f"Script name: {sys.argv[0]}")
    print(f"# of args w/ script name: {len(sys.argv)}")

    prompt = ""
    if len(sys.argv) > 1:
        prompt += sys.argv[1]
        for arg in sys.argv[2:]:
            prompt += " " + arg
        print(f"Prompt: {prompt}")
    else:
        print("No prompts (arguments) provided. Exiting with Code 1.")
        sys.exit(1)

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=prompt)

    print(response.text)
    #print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    #print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
