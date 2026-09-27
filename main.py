import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function
import json
import sys
import time


def generate_content(client,messages):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0.2,
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("Failed API request")
    return response

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set in .env file")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user","content": args.user_prompt},]


    for _ in range(20):

        response=generate_content(client, messages)
        if args.verbose:
            print(f"User prompt:{args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
             for tool_call in message.tool_calls:
                result_message= call_function(tool_call, verbose=args.verbose)
                if not result_message or not result_message.get("content"):
                    raise Exception(f"Function {tool_call.function.name} produced no content")

                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)

             time.sleep(2)
        else:
            print(message.content)
            return
    print("Error: Agent reached maximum iterations without completing the task.")
    sys.exit(1)


if __name__ == "__main__":
    main()
