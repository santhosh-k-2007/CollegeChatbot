from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
from pathlib 
import Path


app = Flask(__name__)

# Load API key from .env file
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

print("API key loaded:", bool(api_key))

if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"reply": "Please type a message!"})

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You are a helpful AI assistant for a college website. "
                "Answer student questions clearly and simply. "
                "If you do not know a college-specific fact, do not invent it. "
                "Ask the student to contact the college office for official details.\n\n"
                f"Student question: {message}"
            )
        )

        reply = response.text or "Sorry bro, I couldn't generate a response."
        return jsonify({"reply": reply})

    except Exception as e:
        print("Chatbot error:", e)
        return jsonify({
            "reply": "Sorry! AI connection-la problem irukku. Please try again."
        }), 500


if __name__== "__main__":
    app.run(debug=True)