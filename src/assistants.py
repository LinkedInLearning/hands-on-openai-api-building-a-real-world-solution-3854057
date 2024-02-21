import os
import time
import glob
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

pattern = "*.json"
json_files = glob.glob(pattern)

for file_path in json_files:
    print(f'Processing file: {file_path}')

    transcript_file = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants"
    )

    client.beta.assistants.files.create(
        assistant_id=assistant.id,
        file_id=transcript_file.id
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
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    still_running = True
    while still_running:
        latest_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        still_running = latest_run.status != "completed"
        if (still_running):
            time.sleep(2)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].content)

while True:
    display_main_menu()