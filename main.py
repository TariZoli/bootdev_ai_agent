import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from functions.prompts import system_prompt
from functions.call_functions import available_functions, call_function

MAX_ITERATIONS = 20


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for iteration in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError("No usage data returned, check API key or model")

        if args.verbose:
            print(f"[Iteration {iteration + 1}] "
                  f"Prompt tokens: {response.usage.prompt_tokens}, "
                  f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)

            if not result_message["content"]:
                raise Exception(f"Function {tool_call.function.name} returned no content")

            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)

    else:
        print(f"Error: the agent used all {MAX_ITERATIONS} iterations without producing "
        "a final response. The model kept requesting tool calls. "
        "Try a more specific prompt, or run with --verbose to see what it was doing.",
        file=sys.stderr,        )
        sys.exit(1)


if __name__ == "__main__":
    main()