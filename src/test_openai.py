import os
from openai import OpenAI


def main():
    # get api key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5", input="Write a one-sentence bedtime story about a unicorn."
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
