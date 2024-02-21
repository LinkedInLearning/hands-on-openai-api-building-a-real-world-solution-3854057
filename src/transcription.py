import glob
import whatsapp_utils
from openai import OpenAI
import os

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)

pattern = "audios\\*.ogg"
ogg_files = glob.glob(pattern)

for file_name in ogg_files:
    file_datetime = whatsapp_utils.extract_datetime_from_filename(file_name)
    print(f"Processing {file_name}")
    audio_file = open(file_name, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        response_format="text",
        file=audio_file,
        temperature=0.2,
        prompt="Miss Jime, Miss Naty"
    )

    moderation_response = client.moderations.create(input=transcription)
    if (moderation_response.results[0].flagged):
        print("ALERT!")
        print(transcription)
        break

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            { "role":"system", "content":"You are a helpful assistant."},
            { "role":"user", "content":
            f"""
            Translate into English the following text that is surrounded by 3 stars (***).
            Create a JSON document with the following elements:
            - {file_datetime.date()}. Put the translated text here.
            - audiofile_datetime. The value must be: {file_datetime}
            ***
            {transcription}
            ***
            """
            }
        ], response_format={"type":"json_object"}
    )

    with open(f"{file_datetime.date()}.json", "w") as file:
        file.write(completion.choices[0].message.content)

    print("Done!")