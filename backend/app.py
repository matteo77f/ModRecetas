import os
from flask import Flask, request, jsonify
from backend.ai_service import generate_recommendations, extract_text_from_image

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/recommend", methods=["POST"])
def recommend():
    body = request.get_json(silent=True)
    recipe_text = None
    preferences = "make it healthier"
    image = None

    if body is not None:
        recipe_text = body.get("recipe_text")
        preferences = body.get("preferences", preferences)
    else:
        recipe_text = request.form.get("recipe_text")
        preferences = request.form.get("preferences", preferences)
        image = request.files.get("image") or request.files.get("file")

    if image and not recipe_text:
        image_bytes = image.read()
        extraction = extract_text_from_image(image_bytes, filename=image.filename)
        if "error" in extraction:
            return jsonify({"error": extraction["error"]}), 400
        recipe_text = extraction.get("text", "")

    if not recipe_text or not isinstance(recipe_text, str):
        return jsonify({"error": "recipe_text is required and must be a string"}), 400

    try:
        ai_response = generate_recommendations(recipe_text, preferences)
    except Exception as exc:
        return jsonify({
            "error": "Internal server error",
            "details": str(exc),
        }), 500

    if not isinstance(ai_response, dict):
        return jsonify({
            "error": "Invalid AI response",
        }), 500

    return jsonify(ai_response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
