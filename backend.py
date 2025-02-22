from flask import Flask, jsonify, request
from flask_cors import CORS
from call import make_call, get_call_transcript_and_audio
import sys
import os
import base64

# Add the analysis-and-api directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'analysis-and-api'))
from analysis import QuestionAnalysis, evaluate_transcript

app = Flask(__name__)
CORS(app)

@app.route('/hi', methods=['GET'])
def hi():
    return jsonify({"message": "Hello!"}), 200

def transform_transcript_to_exchanges(transcript):
    """
    Transform the transcript into a format with exchanges between interviewer and interviewee.
    Each exchange includes the question, answer, feedback, and score.
    """
    # Parse the transcript into question-answer pairs
    lines = transcript.strip().split('\n')
    exchanges = []
    current_question = None
    
    for line in lines:
        if line.startswith("Agent:"):
            current_question = line.replace("Agent:", "").strip()
        elif line.startswith("User:") and current_question is not None:
            answer = line.replace("User:", "").strip()
            # Use QuestionAnalysis to get the score and feedback
            analysis = QuestionAnalysis(current_question, answer)
            result = analysis.return_json()
            
            exchanges.append({
                "interviewer": current_question,
                "interviewee": answer,
                "interviewer_feedback": result.get("data", {}).get("comment", "No feedback available"),
                "score": result.get("data", {}).get("score", 0)
            })
            current_question = None
    
    return {"exchanges": exchanges}

@app.route('/ringring', methods=['GET'])
def make_phone_call():
    try:
        # Get the phone number from query parameters
        phone_number = request.args.get('phone_number')
        
        if not phone_number:
            return jsonify({
                "status": "error",
                "message": "phone_number parameter is required"
            }), 400
            
        # Format the phone number with +1 prefix
        formatted_number = f"+1{phone_number}"
        
        # Make the call with the provided number
        phone_call_response = make_call("+17655306815", formatted_number)
        
        print(phone_call_response)
        print("Agent ID: ", phone_call_response.agent_id)
        print("Call ID: ", phone_call_response.call_id)
        
        # Get transcript and audio
        transcript, audio_file = get_call_transcript_and_audio(phone_call_response.call_id)
        
        # Debug print
        print("\nReceived transcript type:", type(transcript))
        print("Transcript content:")
        print(transcript)
        print("End of transcript\n")
        
        # Process the transcript through evaluate_transcript
        evaluation_results = evaluate_transcript(transcript)
        
        # Transform the transcript into the required format for exchanges
        exchanges = transform_transcript_to_exchanges(transcript)
        
        # Convert audio file to base64
        with open(audio_file, 'rb') as audio:
            audio_bytes = audio.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            audio_data_uri = f"data:audio/mp3;base64,{audio_base64}"
        
        return jsonify({
            "status": "success",
            "exchanges": exchanges["exchanges"],
            "audio_file": audio_data_uri,
            "score_json": evaluation_results
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def run_flask():
    # For production: listen on all interfaces (0.0.0.0)
    # and use the PORT environment variable provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

if __name__ == '__main__':
    # app.run(debug=True)
    run_flask() 