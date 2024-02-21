import os
from openai import OpenAI

MODEL = "gpt-3.5-turbo-1106"

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)

assistant = client.beta.assistants.create(
    name = "KinderLogger",
    instructions="You are an intelligent assistant.",
    tools=[{"type":"retrieval"},{"type":"code_interpreter"}],
    model=MODEL
)

thread = client.beta.threads.create()

def display_main_menu():
    print("\n[KinderLogger Assistant]")
    prompt=input("\nEnter your prompt: ")
    handle_main_menu_option(prompt)

def handle_main_menu_option(prompt):
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=prompt
    )

while True:
    display_main_menu()