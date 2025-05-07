import requests
import json
import uuid
import os
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:5000/api"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_separator():
    print("\n" + "=" * 50 + "\n")


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
        "responseData": {"results": ["result1", "result2"]},
    }

    print("\nRequest Data:")
    print(json.dumps(data, indent=2))

    response = requests.post(f"{BASE_URL}/history", json=data)
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    return user_id, response.json().get("id")


def get_user_history(user_id):
    print(f"\nRetrieving history for user {user_id}...")
    print(f"\nRequest URL: {BASE_URL}/history/user/{user_id}")

    response = requests.get(f"{BASE_URL}/history/user/{user_id}")
    print(f"\nResponse Status: {response.status_code}")
    if response.status_code != 404:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")


def get_specific_entry(entry_id):
    print(f"\nRetrieving specific entry {entry_id}...")
    print(f"\nRequest URL: {BASE_URL}/history/entry/{entry_id}")

    response = requests.get(f"{BASE_URL}/history/entry/{entry_id}")
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")


def delete_entry(entry_id):
    print(f"\nDeleting entry {entry_id}...")
    print(f"\nRequest URL: {BASE_URL}/history/entry/{entry_id}")

    response = requests.delete(f"{BASE_URL}/history/entry/{entry_id}")
    print(f"\nResponse Status: {response.status_code}")


def main():
    while True:
        clear_screen()
        print("History Service Test Program")
        print("This program will demonstrate the functionality of the history service.")
        print("Make sure the history service is running on http://127.0.0.1:5000")
        print("\nOptions:")
        print("1. Create new history entry")
        print("2. Get user history")
        print("3. Get specific entry")
        print("4. Delete entry")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            clear_screen()
            input("Press Enter to create a new history entry...")
            user_id, entry_id = create_history_entry()
            input("\nPress Enter to continue...")

        elif choice == "2":
            clear_screen()
            user_id = input("Enter user ID: ")
            input("Press Enter to retrieve the user's history...")
            get_user_history(user_id)
            input("\nPress Enter to continue...")

        elif choice == "3":
            clear_screen()
            entry_id = input("Enter entry ID: ")
            input("Press Enter to retrieve the specific entry...")
            get_specific_entry(entry_id)
            input("\nPress Enter to continue...")

        elif choice == "4":
            clear_screen()
            entry_id = input("Enter entry ID: ")
            input("Press Enter to delete the entry...")
            delete_entry(entry_id)
            input("\nPress Enter to continue...")

        elif choice == "5":
            print("\nExiting program...")
            break

        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
