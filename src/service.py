from fastapi import FastAPI
from datetime_utils import *
from openai import OpenAI
import os
import time

TODAY = date.today()
START_OF_WEEK, END_OF_WEEK = get_school_week_bounds(date.today())

key = os.environ.get("OPENAI_API_KEY")
assistant_id = os.environ.get("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=key)

app = FastAPI()


@app.post("/message")
async def read_message(message: str):
    if not message:
        return {"message": "No message received."}

    thread = client.beta.threads.create()
    assistant = client.beta.assistants.retrieve(assistant_id)
    client.beta.threads.messages.create(
        thread.id, 
        role="user", 
        content=message)
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
        assistant_id=assistant.id)
    
    still_running = True
    while still_running:
        run_latest = client.beta.threads.runs.retrieve(
            thread_id=thread.id, 
            run_id=run.id)
        still_running = run_latest.status != "completed"
        if still_running:
            time.sleep(2)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content

    return {"message": f"{result}"}