import os
import time
import glob
from openai import OpenAI
from datetime_utils import *

MODEL = "gpt-3.5-turbo-1106"
TODAY = date.today()
START_OF_WEEK, END_OF_WEEK = get_school_week_bounds(date.today())

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)

assistant = client.beta.assistants.create(
    name = "KinderLogger",
    instructions=f"""
    You are an intelligent assistant equipped with a wealth of information contained in various internal files. When addressing user questions, it's essential to rely on this information to formulate your responses. However, it's crucial to present these answers as though they are derived from your own knowledge base, without referencing or hinting at the existence of these files. The user should perceive the assistance you provide as coming directly from your own expertise, without any visible reliance on external sources or annotations. Your role is to seamlessly offer informed responses, creating an impression of innate understanding and proficiency.

    ***IMPORTANT***

    Please review the contents of the uploaded file(s) before answering.
    
    If you don't know an answer, you must respond 'I don't know.'. No other responses will be accepted.
    """,
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
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=f"""
        -----------------
        Today is {TODAY}.
        -----------------
        The current school week goes from {START_OF_WEEK} and {END_OF_WEEK}.
        -----------------
        SEARCH IN ALL THE DOCUMENTS.
        """
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