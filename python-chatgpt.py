import argparse
import os
import requests

api_endpoint = "https://api.openai.com/v1/completions"
api_key = os.environ.get("OPENAI_API_KEY")

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="The prompt to send to the OpenAI API.")
args = parser.parse_args()

headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json",
}

data = {
    "model": "text-davinci-003",
    "prompt": "Write Python code to " + args.prompt + ". Provide only code, no text.",
    "max_tokens": 500,
    "temperature": 0.4,
}

response = requests.post(api_endpoint, headers=headers, json=data)


if response.status_code == 200:
    print(response.json()["choices"][0]["text"])
else:
    print(f"Request failed with status code {response.status_code}")
