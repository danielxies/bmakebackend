import requests
import json
import time

def hit_ringring(phone_number):
    url = f"https://api.meriedith.com/ringring?phone_number={phone_number}"
    
    print(f"Making call request to {phone_number}...")
    print("This may take several minutes while the call completes...")
    response = requests.get(url, timeout=300)  # 5 minute timeout
    
    if response.status_code == 200:
        data = response.json()
        print("\nCall successful!")
        print("Status:", data["status"])
        
        if data["status"] == "success":
            print("\nInterview Results:")
            print("\nExchanges:")
            for exchange in data["exchanges"]:
                print("\nQuestion:", exchange["interviewer"])
                print("Answer:", exchange["interviewee"])
                print("Feedback:", exchange["interviewer_feedback"])
                print("Score:", exchange["score"])
            
            print("\nOverall Evaluation:")
            print(json.dumps(data["score_json"], indent=2))
        else:
            print("Error:", data["message"])
    else:
        print(f"Request failed with status code: {response.status_code}")
        if response.text:
            print("Error message:", response.text)

if __name__ == "__main__":
    # Test with the sample phone number
    hit_ringring("4697717436")
