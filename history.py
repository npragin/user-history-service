from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///history.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define the Budget model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_contents = db.Column(db.LargeBinary, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "budget_contents": base64.b64encode(self.budget_contents).decode("utf-8"),
        }

    @classmethod
    def from_dict(cls, data):
        # Decode base64 string to bytes
        budget_contents = base64.b64decode(data["budgetContents"])
        return cls(
            budget_contents=budget_contents,
        )


# Create database tables
with app.app_context():
    db.create_all()


@app.route("/api/get-all-budget-ids", methods=["GET"])
def get_all_budget_ids():
    budget_ids = db.session.query(Budget.id).all()
    return jsonify({"budgetIDs": [budget_id[0] for budget_id in budget_ids]}), 200


@app.route("/api/swap-budget", methods=["POST"])
def swap_budget():
    data = request.get_json()

    # Validate request body
    required_fields = [
        "oldBudgetID",
        "newBudgetID",
        "oldBudgetContents",
    ]
    if not data or not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        return (
            jsonify({"error": "Missing required fields: " + ", ".join(missing_fields)}),
            400,
        )

    # Update existing budget content
    try:
        existing_budget = db.session.query(Budget).get(data["oldBudgetID"])
        if not existing_budget:
            return jsonify({"error": f"Budget {data['oldBudgetID']} not found"}), 404

        # Decode base64 string to bytes
        existing_budget.budget_contents = base64.b64decode(data["oldBudgetContents"])
        db.session.commit()

        new_budget = db.session.query(Budget).get(data["newBudgetID"])
        if not new_budget:
            return jsonify({"error": f"Budget {data['newBudgetID']} not found"}), 404

        return (
            jsonify(
                {
                    "newBudgetContents": base64.b64encode(
                        new_budget.budget_contents
                    ).decode("utf-8")
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": f"Error swapping budget: {str(e)}"}), 500


@app.route("/api/save-budget", methods=["POST"])
def save_budget():
    data = request.get_json()

    # Validate request body
    required_fields = [
        "budgetID",
        "budgetContents",
    ]
    if not data or not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if not data.get(field)]
        return (
            jsonify({"error": "Missing required fields: " + ", ".join(missing_fields)}),
            400,
        )

    # Save budget
    try:
        budget = db.session.query(Budget).get(data["budgetID"])
        if not budget:
            return jsonify({"error": f"Budget {data['budgetID']} not found"}), 404

        # Decode base64 string to bytes
        budget.budget_contents = base64.b64decode(data["budgetContents"])
        db.session.commit()
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": f"Error saving budget: {str(e)}"}), 500


@app.route("/api/create-budget", methods=["POST"])
def create_budget():
    data = request.get_json()

    # Validate request body
    required_fields = [
        "budgetContents",
    ]
    if not data or not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if not data.get(field)]
        return (
            jsonify({"error": "Missing required fields: " + ", ".join(missing_fields)}),
            400,
        )

    # Create budget
    try:
        budget = Budget.from_dict(data)
        db.session.add(budget)
        db.session.commit()
        return jsonify({"newBudgetID": budget.id}), 200
    except Exception as e:
        return jsonify({"error": f"Error creating budget: {str(e)}"}), 500


@app.route("/api/delete-budget/<int:budget_id>", methods=["DELETE"])
def delete_budget(budget_id):
    try:
        budget = Budget.query.get(budget_id)
        if not budget:
            return jsonify({"error": f"Budget {budget_id} not found"}), 404

        db.session.delete(budget)
        db.session.commit()
        return jsonify({"message": f"Budget {budget_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error deleting budget: {str(e)}"}), 500


@app.route("/api/load-budget/<budget_id>", methods=["GET"])
def load_budget(budget_id):
    try:
        budget = db.session.query(Budget).get(budget_id)
        if not budget:
            return jsonify({"error": f"Budget {budget_id} not found"}), 404

        encoded = base64.b64encode(budget.budget_contents).decode("utf-8")
        return jsonify({"budgetContents": encoded}), 200

    except Exception as e:
        return jsonify({"error": f"Error loading budget: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
