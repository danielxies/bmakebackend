import os
from retell import Retell
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RETELL_API_KEY")
print(f"API Key:", API_KEY)

client = Retell(
    api_key=API_KEY,
)

call_id = "call_38fe4784fe960f9401ed94fc5df"

def get_call_transcript(call_id: str):
    # Retrieve the transcript using the Retell SDK
    transcript_response = client.call.get_transcript(call_id=call_id)
    # Return the transcript text
    return transcript_response.text

transcript = get_call_transcript(call_id)
print("Transcript: \n", transcript)