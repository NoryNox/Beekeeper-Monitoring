from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Deine E-Mail-Config (gratis Gmail oder Outlook)
EMAIL_USER = "deine-email@gmail.com"  # Deine Gmail (aktiviere "Weniger sichere Apps" oder App-Passwort)
EMAIL_PASS = "dein-app-passwort"  # Gmail App-Passwort (gratis)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Carrier-SMS-Gateways (DE, gratis)
CARRIERS = {
    'telekom': 'sms.telekom.de',  # 0170, 0171, 0175
    'vodafone': 'sms.vodafone.de',  # 0172, 0178
    'o2': 'o2online.de',  # 0176
    'eplus': 'smsmail.eplus.de',  # 0177
    'generic': 't-mobile-sms.de'  # Fallback
}

def get_carrier(phone):
    num = phone.replace('+49', '').replace(' ', '')
    if num.startswith(('170', '171', '175')): return 'telekom'
    if num.startswith(('172', '178')): return 'vodafone'
    if num.startswith('176'): return 'o2'
    if num.startswith('177'): return 'eplus'
    return 'generic'

@app.route('/api/alarm', methods=['POST'])
def alarm():
    data = request.json or {}
    score = data.get('score', 0)
    phone = data.get('phone', '').strip()
    message = data.get('message', f"Beekeeper-Alarm! Bedrohung erkannt (Score: {int(score*100)}%)")

    if not phone or not phone.startswith('+49'):
        return jsonify({"status": "error", "message": "Ungültige DE-Nummer (+49...)"}), 400

    carrier = get_carrier(phone)
    sms_email = phone.replace('+49', '') + '@' + CARRIERS[carrier]

    try:
        msg = MIMEText(message)
        msg['Subject'] = 'Beekeeper Alarm'
        msg['From'] = EMAIL_USER
        msg['To'] = sms_email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, sms_email, text)
        server.quit()
        print(f"SMS per E-Mail an {phone} gesendet – Carrier: {carrier}")
        return jsonify({"status": "success", "message": "SMS versendet!"})
    except Exception as e:
        print(f"Send-Fehler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
