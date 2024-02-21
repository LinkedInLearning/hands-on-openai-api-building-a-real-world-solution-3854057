from openai import OpenAI
import os

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)