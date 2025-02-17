import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your WhatsApp Cloud API credentials
ACCESS_TOKEN = "your_access_token"  # Replace with your access token
PHONE_NUMBER_ID = "your_phone_number_id"  # Replace with your phone number ID
WHATSAPP_API_URL = f"https://graph.facebook.com/v15.0/{PHONE_NUMBER_ID}/messages"

# Function to send message
def send_whatsapp_message(to, message):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    response = requests.post(WHATSAPP_API_URL, json=data, headers=headers)
    return response.json()

# Webhook to receive messages
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)  # To log incoming message data (for debugging)
    
    # Check if the message is a WhatsApp message
    if 'messages' in data['entry'][0]['changes'][0]['value']:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        phone_number = message['from']
        text = message['text']['body']
        
        # Here you can add your logic to respond
        response_text = f"You said: {text}"  # Simple echo bot for now
        
        # Send response
        send_whatsapp_message(phone_number, response_text)
    
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
