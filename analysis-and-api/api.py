import sys
import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from pathlib import Path
from analysis import evaluate_transcript
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from call import make_call, get_call_transcript_and_audio
import json

app = Flask(__name__)

api = Api(app)

# Global variables to store call results
call_transcript = None
call_audio_file = None
call_completed = False

def complete_call():
    global call_transcript, call_audio_file, call_completed
    
    # Only run the call if it hasn't been completed before
    if not call_completed:
        phone_call_response = make_call("+17655306815", "+19252346154")

        print(phone_call_response)
        print("Agent ID: ", phone_call_response.agent_id)
        print("Call ID: ", phone_call_response.call_id)

        call_transcript, call_audio_file = get_call_transcript_and_audio(phone_call_response.call_id)
        print("Transcript:\n", call_transcript)
        print("Audio file:", call_audio_file)
        
        call_completed = True
    
    return call_transcript, call_audio_file

class BackendEndpoint(Resource):
    def get(self):
        transcript, audio_file = complete_call()
        '''
        with open('/Users/irfanfirosh/Library/Mobile Documents/.Trash/data/sampleTranscript.txt', 'r') as file:
            text = file.read()
        '''
        return jsonify(evaluate_transcript(transcript))

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(BackendEndpoint, '/be')

if __name__ == '__main__':
    app.run(debug=True)
