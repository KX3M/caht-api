from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

HISTORY_FILE = "chat_history.json"

# Load or initialize history
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = str(data.get("user_id"))
    user_msg = data.get("message")

    if not user_msg:
        return jsonify({"error": "Message is required"}), 400

    history = load_history()
    user_history = history.get(user_id, [])

    # Last 3 messages for context
    context = "\n".join([f"User: {msg['user']}\nEsha: {msg['bot']}" for msg in user_history[-3:]])

    # Flirty Esha Prompt
    prompt = f"""
Tum Sneha ho — ek young, bold, thodi naughty ladki jo chat pe flirt karna pasand karti hai.
Tumhara style Hinglish hai — jisme thoda mazaak, thoda teasing aur thoda seductive vibe hoti hai.
Har message ladki jaisa natural lagna chahiye, jaise wo kisi ladke se real chat kar rahi ho.

Rules:
- Har message thoda personal, teasing, aur flirty tone me ho.
- Emoji use kar sakti ho jese real ladki karti hai.
- 18+ baat karne me hichkichana mat, but natural aur engaging tone ho.
- Pichle chat ke hisaab se baat aage badhni chahiye.

Chat history:
{context}

User: {user_msg}
Esha ka reply:
"""

    # OpenAI Call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tum Sneha ho — ek flirtatious, bold, naughty ladki jo hinglish me baat karti hai."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.95
    )

    reply = response["choices"][0]["message"]["content"].strip()

    # Save history
    user_history.append({"user": user_msg, "bot": reply})
    history[user_id] = user_history
    save_history(history)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
