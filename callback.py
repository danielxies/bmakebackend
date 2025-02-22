from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/retell/callback", methods=["POST"])
def retell_callback():
    data = request.json  # Parse the incoming JSON payload
    call_id = data.get("call_id")
    status = data.get("status")
    transcript = data.get("transcript")  # Assuming Retell provides this directly

    print(f"Received callback for Call ID: {call_id}, Status: {status}")

    # Store the transcript or process it further
    if transcript:
        print("Transcript:\n", transcript)

    return jsonify({"message": "Callback received"}), 200

if __name__ == "__main__":
    app.run(port=5000)
