import requests

def test_transcript_endpoint():
    # Base URL - replace with your actual server URL
    base_url = "http://localhost:5000"  # or your actual server URL
    
    # Test endpoint
    endpoint = f"{base_url}/get_transcript"
    
    # Test data
    test_data = {
        "call_id": "call_38fe4784fe960f9401ed94fc5df"
    }
    
    try:
        # Make the POST request
        response = requests.post(endpoint, json=test_data)
        
        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_transcript_endpoint() 