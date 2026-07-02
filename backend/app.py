import os
from flask import Flask, request, jsonify
from backend.ai_service import generate_recommendations

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/recommend", methods=["POST"])
def recommend():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "JSON body is required"}), 400

    recipe_text = body.get("recipe_text")
    preferences = body.get("preferences", "make it healthier")

    if not recipe_text or not isinstance(recipe_text, str):
        return jsonify({"error": "recipe_text is required and must be a string"}), 400

    ai_response = generate_recommendations(recipe_text, preferences)
    return jsonify(ai_response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
