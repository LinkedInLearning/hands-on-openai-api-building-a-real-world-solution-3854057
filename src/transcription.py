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