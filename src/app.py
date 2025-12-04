from flask import Flask, request, jsonify
import smtplib, random, time
from email.mime.text import MIMEText

app = Flask(__name__)

# Deine Gmail-Daten (kostenlos)
EMAIL = "deine.email@gmail.com"           # ← deine Gmail
APP_PASS = "dein-app-passwort"            # ← App-Passwort aus Google-Konto
codes = {}  # {contact: (code, timestamp)}

# SMS-Gateways (Deutschland – kostenlos!)
CARRIERS = {
    'telekom': 'sms.telekom.de',
    'vodafone': 'sms.vodafone.de',
    'o2': 'o2online.de',
    'eplus': 'smsmail.eplus.de'
}

def send_email(to_email, code):
    msg = MIMEText(f"Dein Beekeeper-Code: {code}\nGültig 10 Minuten.")
    msg['Subject'] = "Beekeeper Monitoring – Bestätigungscode"
    msg['From'] = EMAIL
    msg['To'] = to_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, APP_PASS)
        server.sendmail(EMAIL, to_email, msg.as_string())

def send_sms(phone, code):
    num = phone.replace('+49','').replace(' ','')
    carrier = 'telekom' if num.startswith(('170','171','175')) else 'vodafone' if num.startswith(('172','178')) else 'o2' if num.startswith('176') else 'eplus'
    sms_email = f"{num}@{CARRIERS.get(carrier, 't-mobile-sms.de')}"
    send_email(sms_email, code)

@app.route('/api/send-code', methods=['POST'])
def send_code():
    contact = request.json.get('contact','').strip()
    if not contact: return jsonify({"status":"error","message":"Kein Kontakt"}), 400
    
    code = random.randint(100000,999999)
    codes[contact] = (code, time.time())
    
    if '@' in contact:
        send_email(contact, code)
    else:
        send_sms(contact, code)
    
    return jsonify({"status":"success"})

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    contact = request.json.get('contact')
    code = request.json.get('code')
    if contact not in codes: return jsonify({"status":"error","message":"Kein Code"}), 400
    
    saved_code, timestamp = codes[contact]
    if time.time() - timestamp > 600: 
        del codes[contact]
        return jsonify({"status":"error","message":"Code abgelaufen"}), 400
    
    if str(saved_code) == str(code):
        del codes[contact]
        return jsonify({"status":"success"})
    return jsonify({"status":"error","message":"Falscher Code"}), 400

@app.route('/api/alarm', methods=['POST'])
def alarm():
    phone = request.json.get('phone','')
    score = request.json.get('score',0)
    message = f"Beekeeper-Alarm! Bedrohung erkannt (Score: {int(score*100)}%)"
    if phone and phone.startswith('+'):
        send_sms(phone, message)
    return jsonify({"status":"success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)), debug=True)
