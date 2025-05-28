import requests
import json
import pickle
import base64
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:5000/api"

def print_separator():
    print("\n" + "=" * 50 + "\n")

def demonstrate_create_budget():
    """Demonstrate creating a new budget"""
    print("Demonstrating budget creation...")
    
    # Sample budget data
    budget_data = {
        "name": "Monthly Budget",
        "amount": 5000,
        "categories": ["groceries", "utilities", "entertainment"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    print("\nCreating budget with data:")
    print(json.dumps(budget_data, indent=2))
    
    # Pickle and base64 encode the budget data
    pickled_data = pickle.dumps(budget_data)
    encoded_data = base64.b64encode(pickled_data).decode('utf-8')
    
    response = requests.post(
        f"{BASE_URL}/create-budget",
        json={"budgetContents": encoded_data}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    return response.json().get("newBudgetID")

def demonstrate_save_budget(budget_id):
    """Demonstrate saving an existing budget"""
    print("\nDemonstrating budget save...")
    
    # Modified budget data
    updated_data = {
        "name": "Updated Monthly Budget",
        "amount": 6000,
        "categories": ["groceries", "utilities", "entertainment", "savings"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    print(f"\nSaving budget {budget_id} with updated data:")
    print(json.dumps(updated_data, indent=2))
    
    # Pickle and base64 encode the updated data
    pickled_data = pickle.dumps(updated_data)
    encoded_data = base64.b64encode(pickled_data).decode('utf-8')
    
    response = requests.post(
        f"{BASE_URL}/save-budget",
        json={
            "budgetID": budget_id,
            "budgetContents": encoded_data
        }
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")

def demonstrate_swap_budget(budget1_id):
    """Demonstrate swapping budgets"""
    print("\nDemonstrating budget swap...")
    
    # Create a second budget
    budget2_data = {
        "name": "Alternative Budget",
        "amount": 4000,
        "categories": ["rent", "transport", "dining"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    print("\nCreating second budget:")
    print(json.dumps(budget2_data, indent=2))
    
    # Pickle and base64 encode the second budget data
    pickled_data = pickle.dumps(budget2_data)
    encoded_data = base64.b64encode(pickled_data).decode('utf-8')
    
    response = requests.post(
        f"{BASE_URL}/create-budget",
        json={"budgetContents": encoded_data}
    )
    budget2_id = response.json().get("newBudgetID")
    
    print(f"\nSwapping budgets {budget1_id} and {budget2_id}")
    response = requests.post(
        f"{BASE_URL}/swap-budget",
        json={
            "oldBudgetID": budget1_id,
            "newBudgetID": budget2_id,
            "oldBudgetContents": encoded_data
        }
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")

def main():
    print("Budget Service Demonstration")
    print("This program demonstrates the three main endpoints of the budget service.")
    print("Make sure the budget service is running on http://127.0.0.1:5000")
    
    print_separator()
    
    # Demonstrate all three endpoints
    budget_id = demonstrate_create_budget()
    print_separator()
    
    demonstrate_save_budget(budget_id)
    print_separator()
    
    demonstrate_swap_budget(budget_id)
    print_separator()
    
    print("Demonstration complete!")

if __name__ == "__main__":
    main()
