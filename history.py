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


@app.route("/api/history", methods=["POST"])
def create_history():
    data = request.get_json()

    # Check if the request body contains required fields
    required_fields = [
        "userId",
        "query",
        "parameters",
        "timestamp",
        "tags",
        "notes",
        "responseData",
    ]
    if not data or not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        return (
            jsonify({"error": "Missing required fields: " + ", ".join(missing_fields)}),
            400,
        )

    if "results" not in data["responseData"]:
        return jsonify({"error": "Missing required field: results"}), 400

    # Validate UUID format
    try:
        uuid.UUID(data["userId"])
    except ValueError:
        return jsonify({"error": "Invalid UUID format for userId"}), 400

    # Add the entry to the database
    try:
        new_entry = SearchHistory.from_dict(data)
        db.session.add(new_entry)
        db.session.commit()
        return (
            jsonify(
                {
                    "id": new_entry.id,
                    "status": "success",
                    "message": "Search history recorded successfully",
                    "timestamp": dt.now(datetime.UTC).isoformat()[:-3] + "Z",
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"error": f"Invalid timestamp format: {str(e)}"}), 400


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
