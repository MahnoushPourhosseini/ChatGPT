# fixing the error: Failed to get a response from the server.
import asyncio
import logging
import json
from openai import OpenAI
from quart import Quart, request, jsonify
from quart_cors import cors

logging.basicConfig(level=logging.DEBUG)
   
app = Quart(__name__)
app = cors(app, allow_origin="*")  # Allow all origins for development
client = OpenAI(api_key="")
CHAT_HISTORY_FILE = "chat_history.json"

# Helper function to load chat history
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Helper function to save chat history
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Chat route for handling user input and OpenAI API calls
@app.route('/chat', methods=['POST'])
async def chat():
    try:
        # Get data from frontend
        data = await request.get_json()
        logging.debug(f"Received request data: {data}")
        user_message = data.get("messages", [{}])[0].get("content", "")

        if not user_message:
            return jsonify({"error": "No message content provided"}), 400

        # Prepare messages for OpenAI
        messages = [
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": user_message }
        ]

        # Make an API call to OpenAI
        # response = await asyncio.to_thread(
        #     client.chat.completions.create(
        #     model="gpt-3.5-turbo",  # Use GPT-4 if accessible
        #     messages=messages)
        # )
        response = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1696438900,
            "model": "gpt-3.5-turbo",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This is a dummy response generated to test your application logic."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 15,
                "total_tokens": 25
            }
        }
  
        # Extract the chatbot's reply
        chatbot_reply = response['choices'][0]['message']['content']

        # Update chat history
        # history = load_chat_history()
       
        # history.append({ "role": "user", "content": user_message })
        # history.append({ "role": "assistant", "content": chatbot_reply })
        # save_chat_history(history)

        # Return chatbot's reply
        return jsonify({"answer": chatbot_reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get chat history
@app.route('/history', methods=['GET'])
async def get_history():
    try:
        # Load and return the chat history
        history = load_chat_history()
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Quart app
if __name__ == "__main__":
    app.run(debug=True)
