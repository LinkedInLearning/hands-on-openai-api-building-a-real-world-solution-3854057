from fastapi import FastAPI


app = FastAPI()


@app.post("/message")
async def read_message(message: str):


    if not message:
        return {"message": "No message received."}
   
    return {"message": f"{message}"}