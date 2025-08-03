from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import cohere

app = Flask(__name__)

# 🔑 Replace this with your actual Cohere API key
cohere_api_key = "qLTHL9OycLbwnvk6YGGR7ezo4fKD0UkVFG3MG9aG"
co = cohere.Client(cohere_api_key)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    print(f"User said: {incoming_msg}")

    try:
        # ✅ Use Cohere's chat model properly
        response = co.chat(
            model="command-r",  # Or "command-r+" if you want the best results
            message=incoming_msg,
            chat_history=[],
            temperature=0.7
        )
        reply = response.text

    except Exception as e:
        print("Cohere error:", e)
        reply = "Sorry, I couldn't generate a response."

    # ✅ Send reply back to WhatsApp
    twilio_resp = MessagingResponse()
    msg = twilio_resp.message()
    msg.body(reply)

    return str(twilio_resp)

if __name__ == "__main__":
    app.run(port=5000)
