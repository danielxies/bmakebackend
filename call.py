import os
import time 
import requests
import base64
from retell import Retell
from retell.resources.call import CallResource
from keys import Keys

client = Retell(
    api_key=Keys.RETELL_API_KEY,
)

# make a call using interviewer and interviewee 
def make_call(interviewer, interviewee):
    return client.call.create_phone_call(
        from_number=interviewer,
        to_number=interviewee,
    )

def get_call_transcript_and_audio(call_id: str):
    call_resource = CallResource(client)
    while True:
        call_response = call_resource.retrieve(call_id=call_id)
        response_data = call_response.dict()
        
        # Check if call has ended
        if response_data.get("call_status") == "ended":
            time.sleep(5)
            transcript = response_data.get("transcript", "No transcript available.")
            recording_url = response_data.get("recording_url")
            
            if recording_url:
                print(f"Downloading audio from: {recording_url}")
                audio_file = download_audio(recording_url, call_id)
                return transcript, audio_file
            else:
                print("No recording URL found.")
                return transcript, None
        else:
            print(f"Call status: {response_data.get('call_status', 'Unknown')} - waiting for call to end...")
            time.sleep(5)

def download_audio(url, call_id):
    """Downloads the call audio and returns it as a base64 data URI."""
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        # Read the entire response content
        audio_data = response.content
        # Convert to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        # Create data URI
        audio_data_uri = f"data:audio/wav;base64,{audio_base64}"
        print(f"Audio data converted to base64")
        return audio_data_uri
    else:
        print(f"Failed to download audio. Status code: {response.status_code}")
        return None
