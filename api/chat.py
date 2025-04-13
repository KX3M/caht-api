import openai
import os
import json
from urllib.parse import unquote

# Set OpenAI API Key
openai.api_key = os.getenv("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")

# Load chat history from a JSON file
def load_chat_history():
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save chat history to a JSON file
def save_chat_history(chat_history):
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f, indent=4)

# Main function to handle requests
def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    # Extract 'user_id' and 'message' from the query parameters
    user_id = request.query_params.get("user_id", "user")
    user_msg = unquote(request.query_params.get("message", ""))  # Decode the URL-encoded message

    if not user_msg:
        return {"statusCode": 400, "body": "Message is required"}

    # Load the chat history for the user
    chat_history = load_chat_history()

    # If user has history, use it as context for the current message
    if user_id in chat_history:
        history = chat_history[user_id]
    else:
        history = []

    # Add the new user message to the chat history
    history.append({"role": "user", "message": user_msg})

    # Construct the conversation prompt for the AI model
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
    """
    
    # Add the previous chat history to the prompt
    for msg in history:
        prompt += f"{msg['role'].capitalize()}: {msg['message']}\n"

    # Add the new user message to the prompt
    prompt += f"User: {user_msg}\nSneha ka reply:"

    # Make OpenAI API call
    response = openai.Completion.create(
        model="text-davinci-003",  # You can use gpt-4 if you prefer
        prompt=prompt,
        max_tokens=150,
        temperature=0.9
    )

    # Get the reply from OpenAI
    reply = response["choices"][0]["text"].strip()

    # Add the assistant's response to history
    history.append({"role": "assistant", "message": reply})

    # Save updated chat history
    chat_history[user_id] = history
    save_chat_history(chat_history)

    # Return the reply as JSON
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": reply})
    }
    
