import os
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.environ["openai_api_key"]

# Interview Questions
response = openai.Completion.create(
    engine="davinci-instruct-beta",
    prompt="You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend:",
    temperature=0.8,
    max_tokens=64,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,

)

print(response)
