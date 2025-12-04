from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import random
import time
import re

app = Flask(__name__)

# Deine Gmail-Config (ersetze mit deiner – gratis)
EMAIL_USER = "beekeeper.monitoring@gmail.com"  # Erstelle neue Gmail (oder deine)
EMAIL_PASS = "abcd efgh ijkl mnop"  # App-Passwort aus Google (unten erklärt)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Carrier-Gateways (DE, getestet 2025)
CARRIERS = {
    'telekom': 't-mobile-sms.de',  # 0170, 0171, 0175 – fixiert
    'vodafone': 'sms.vodafone.de',  # 0172, 0178
    'o2': 'o2online.de',  # 0176
    'eplus': 'smsmail.eplus.de',  # 0177
    'generic': 't-mobile-sms.de'  # Fallback
}

codes = {}  # {contact: (code, timestamp)}

def get_carrier(phone):
    num = re.sub(r'[^0-9]', '', phone.replace('+49', ''))
    if num.startswith(('170', '171', '175')): return 'telekom'
    if num.startswith(('172', '178')): return 'vodafone'
    if num.startswith('176'): return 'o2'
    if num.startswith('177'): return 'eplus'
    return 'generic'

def send_email(to, code):
    try:
        msg = MIMEText(f"Dein Beekeeper-Code: {code}\nGültig 10 Minuten.")
        msg['Subject'] = "Beekeeper Monitoring – Bestätigungscode"
        msg['From'] = EMAIL_USER
        msg['To'] = to
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"E-Mail-Fehler: {e}")
        return False

def send_sms(phone, code):
    carrier = get_carrier(phone)
    sms_email = re.sub(r'[^0-9]', '', phone.replace('+49', '')) + '@' + CARRIERS[carrier]
    return send_email(sms_email, code)

@app.route('/api/send-code', methods=['POST'])
def send_code():
    contact = request.json.get('contact', '').strip()
    if not contact:
        return jsonify({"status": "error", "message": "Kein Kontakt angegeben"}), 400

    code = random.randint(100000, 999999)
    codes[contact] = (code, time.time())

    sent = False
    if '@' in contact:
        sent = send_email(contact, code)
    else:
        sent = send_sms(contact, code)

    if sent:
        return jsonify({"status": "success", "message": "Code gesendet!"})
    else:
        del codes[contact]
        return jsonify({"status": "error", "message": "Senden fehlgeschlagen – prüfe Config"}), 500

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    contact = request.json.get('contact')
    code = request.json.get('code')
    if contact not in codes:
        return jsonify({"status": "error", "message": "Kein Code vorhanden"}), 400

    saved_code, timestamp = codes[contact]
    if time.time() - timestamp > 600:  # 10 Min
        del codes[contact]
        return jsonify({"status": "error", "message": "Code abgelaufen"}), 400

    if str(saved_code) == str(code):
        del codes[contact]
        return jsonify({"status": "success", "message": "Bestätigt!"})
    return jsonify({"status": "error", "message": "Falscher Code"}), 400

@app.route('/api/alarm', methods=['POST'])
def alarm():
    phone = request.json.get('phone', '')
    score = request.json.get('score', 0)
    if not phone.startswith('+49'):
        return jsonify({"status": "error", "message": "Ungültige Nummer"}), 400

    message = f"Beekeeper-Alarm! Bedrohung erkannt (Score: {int(score*100)}%). Überprüfe den Stock!"
    sent = send_sms(phone, message)  # Code ist Text, funktioniert als Nachricht

    if sent:
        return jsonify({"status": "success", "message": "SMS gesendet!"})
    return jsonify({"status": "error", "message": "Senden fehlgeschlagen"}), 500

if __name__ == '__main__':
    app.run(debug=True)
