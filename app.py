from flask import Flask, request
import os, requests

app = Flask(__name__)

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
HEADERS = {"Authorization": f"Bearer " + API_KEY, "Content-Type": "application/json"}

def get_record(table, record_id):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table}/{record_id}"
    r = requests.get(url, headers=HEADERS)
    return r.json()

@app.route("/")
def home():
    return "🟢 Сервер работает."

@app.route("/process", methods=["GET"])
def process():
    record_id = request.args.get("recordId")
    if not record_id:
        return "❌ Нет recordId", 400

    record = get_record("Персонал", record_id)
    roles = record["fields"].get("Роли", [])

    if "R.17" in roles:
        return "✅ Роль подтверждена. Запись обработана.", 200
    else:
        return "❌ Недостаточно прав.", 403
