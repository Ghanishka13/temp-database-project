from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()

app = Flask(__name__)

def init_firebase():
    if not firebase_admin._apps:
        cred_dict = {
            "type": os.getenv("FIREBASE_TYPE"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })

init_firebase()

@app.route("/send", methods=["POST"])
def receive_temperature():
    data = request.json
    temperature = data.get("temperature")
    humidity = data.get("humidity", "")

    if temperature is None:
        return {"status": "error", "message": "No temperature received"}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        ref = db.reference("Temp/Time/data")
        new_data = {
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity
        }
        ref.push(new_data)
        print(f"[OK] {timestamp} - Temp: {temperature}C | Firebase Saved")
        return {"status": "success", "message": "Data saved to Firebase"}
    
    except Exception as e:
        print(f"[ERROR] Firebase Error: {e}")
        return {"status": "error", "message": f"Firebase Error: {e}"}

@app.route("/sync", methods=["POST"])
def sync_firebase():
    print("\n[SYNC] Manual sync triggered...")
    os.system("python fetch_firebase.py")
    return {"status": "success", "message": "Firebase sync completed"}

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  SERVER RUNNING (FIREBASE MODE)")
    print("="*50)
    print("Endpoints:")
    print("  • POST /send - Save temperature to Firebase")
    print("  • POST /sync - Manual sync Firebase→Excel/CSV")
    print("\nExample (ESP32):")
    print("  curl -X POST http://YOUR_PC_IP:5000/send \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"temperature\":28.5,\"humidity\":65}'")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=5000)
