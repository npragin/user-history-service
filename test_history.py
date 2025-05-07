import requests
import json
import uuid
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:5000/api"

def print_separator():
    print("\n" + "="*50 + "\n")

def create_history_entry():
    print("Creating a new history entry...")
    
    # Generate a random UUID for the user
    user_id = str(uuid.uuid4())
    
    # Create sample data
    data = {
        "userId": user_id,
        "query": "test query",
        "parameters": {"param1": "value1", "param2": "value2"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tags": ["test", "demo"],
        "notes": "This is a test entry",
        "responseData": {
            "results": ["result1", "result2"]
        }
    }
    
    response = requests.post(f"{BASE_URL}/history", json=data)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    return user_id, response.json().get("id")

def get_user_history(user_id):
    print(f"\nRetrieving history for user {user_id}...")
    response = requests.get(f"{BASE_URL}/history/user/{user_id}")
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")

def get_specific_entry(entry_id):
    print(f"\nRetrieving specific entry {entry_id}...")
    response = requests.get(f"{BASE_URL}/history/entry/{entry_id}")
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")

def delete_entry(entry_id):
    print(f"\nDeleting entry {entry_id}...")
    response = requests.delete(f"{BASE_URL}/history/entry/{entry_id}")
    print(f"Response Status: {response.status_code}")

def main():
    print("History Service Test Program")
    print("This program will demonstrate the functionality of the history service.")
    print("Make sure the history service is running on http://127.0.0.1:5000")
    
    input("\nPress Enter to create a new history entry...")
    user_id, entry_id = create_history_entry()
    
    input("\nPress Enter to retrieve the user's history...")
    get_user_history(user_id)
    
    input("\nPress Enter to retrieve the specific entry...")
    get_specific_entry(entry_id)
    
    input("\nPress Enter to delete the entry...")
    delete_entry(entry_id)
    
    print("\nTest program completed!")

if __name__ == "__main__":
    main()
