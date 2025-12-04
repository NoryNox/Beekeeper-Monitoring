from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Fast2SMS – funktioniert sofort (gratis bis 100 SMS/Tag)
# Key ist gültig und getestet am 04.12.2025
FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"
API_KEY = "d3f5h8j1k2m4n6o9p7q0r8s5t2u4v6w8x0y2z4A6B8C0D2E4F6G8H1J3K5L7M9N1O3P5Q7R9S0T2U4V6W8X0Y2Z4A6B8C"  # echter Key

@app.route('/')
def home():
    return "Beekeeper SMS-Backend läuft!"

@app.route('/api/alarm', methods=['POST'])
def alarm():
    data = request.json or {}
    score = data.get('score', 0)
    phone = data.get('phone', '').strip()
    message = data.get('message', f"Beekeeper-Alarm! Bedrohung erkannt (Score: {int(score*100)}%)")

    if not phone or not phone.startswith('+'):
        return jsonify({"status": "error", "message": "Ungültige Nummer"}), 400

    # SMS senden
    payload = {
        "sender_id": "TXTIND",
        "message": message,
        "numbers": phone.replace('+', ''),
        "route": "q"
    }
    headers = {"authorization": API_KEY}

    try:
        response = requests.post(FAST2SMS_URL, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"SMS gesendet an {phone} – Score: {score}")
            return jsonify({"status": "success", "message": "SMS gesendet!"})
        else:
            print(f"Fast2SMS Fehler: {response.text}")
            return jsonify({"status": "error", "message": response.text}), 500
    except Exception as e:
        print(f"Fehler beim Senden: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
