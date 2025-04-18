from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import datetime

app = Flask(__name__)
CORS(app)

journal_entries = []

@app.route("/api/entries", methods=["GET"])
def get_entries():
    return jsonify(journal_entries)

@app.route("/api/entries", methods=["POST"])
def add_entry():
    data = request.json
    content = data.get("content", "")
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    analysis = TextBlob(content)
    polarity = analysis.sentiment.polarity
    mood = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

    entry = {
        "id": len(journal_entries) + 1,
        "content": content,
        "date": date,
        "mood": mood
    }
    journal_entries.append(entry)
    return jsonify(entry), 201

if __name__ == "__main__":
    app.run(debug=True)
