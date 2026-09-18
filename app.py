from flask import Flask, render_template, request, jsonify
from utils.openai_client import OpenAIClient
import os

app = Flask(__name__)

client = OpenAIClient()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    question = request.form.get("question", "").strip()
    image = request.files.get("image")

    if not question and not image:
        return jsonify({
            "answer": "Please enter a question or upload an image."
        })

    image_path = None

    if image:
        image_path = os.path.join(
            "static",
            "uploaded_image.jpg"
        )

        image.save(image_path)

    answer = client.ask(
        question,
        image_path=image_path
    )

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)