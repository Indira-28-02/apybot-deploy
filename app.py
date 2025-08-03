from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import cohere
import os

app = Flask(_name_)

# Load Cohere API key from environment variable
cohere_api_key = os.environ.get("qLTHL9OycLbwnvk6YGGR7ezo4fKD0UkVFG3MG9aG")
co = cohere.Client(cohere_api_key)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    print(f"User said: {incoming_msg}")

    try:
        response = co.chat(
            model="command-r",  # Or "command-r+" if available
            message=incoming_msg,
            chat_history=[],
            temperature=0.7
        )
        reply = response.text
    except Exception as e:
        print("Cohere error:", e)
        reply = "Sorry, I couldn't generate a response."

    twilio_resp = MessagingResponse()
    msg = twilio_resp.message()
    msg.body(reply)

    return str(twilio_resp)

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)