from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
            "budget_contents": self.budget_contents,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            budget_contents=data["budget_contents"],
        )


# Create database tables
with app.app_context():
    db.create_all()


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

        existing_budget.budget_contents = data["oldBudgetContents"]
        db.session.commit()

        new_budget = db.session.query(Budget).get(data["newBudgetID"])
        if not new_budget:
            return jsonify({"error": f"Budget {data['newBudgetID']} not found"}), 404

        return jsonify({"newBudgetContents": new_budget.budget_contents}), 200
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

        budget.budget_contents = data["budgetContents"]
        db.session.commit()
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": f"Error saving budget: {str(e)}"}), 500


@app.route("/api/history/user/<uuid:user_id>", methods=["GET"])
def get_history(user_id):
    entries = (
        db.session.query(SearchHistory)
        .filter_by(user_id=str(user_id))
        .order_by(SearchHistory.timestamp.desc())
        .all()
    )
    return jsonify([entry.to_dict() for entry in entries])


@app.route("/api/history/entry/<uuid:user_id>/<int:id>", methods=["GET"])
def get_history_entry(_, id):
    entry = db.session.query(SearchHistory).get_or_404(id)
    return jsonify(entry.to_dict())


@app.route("/api/history/entry/<uuid:user_id>/<int:id>", methods=["DELETE"])
def delete_history_entry(_, id):
    entry = db.session.query(SearchHistory).get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
