import requests
import json

def test_api():
    try:
        response = requests.post('http://localhost:5000/api/chat', 
                               json={"message": "tôi buồn", "user_id": "test"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api() 