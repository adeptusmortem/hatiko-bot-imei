from flask import Flask, render_template, request, jsonify
import json
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response_data = None

    if request.method == "POST":
        # Получаем данные из формы
        imei = request.form.get("imei")
        token = request.form.get("token")

        # Запрашиваем данные от API
        url = "https://api.imeicheck.net/v1/checks"
        payload = json.dumps({
            "deviceId": imei,
            "serviceId": 12
        })
        headers = {
            'Authorization': 'Bearer ' + token,
            'Accept-Language': 'en',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        # Проверяем успешность запроса
        if response.status_code == 201:  # 201 - Created
            response_data = response.json()  # Получаем ответ от API
        else:
            response_data = {"error": "Ошибка при отправке данных на API"}
        
        if len(imei) != 15 or not imei.isdigit():
            return jsonify({"error": "Invalid IMEI"}), 400
        
    return render_template("index.html", data=response_data)

if __name__ == "__main__":
    app.run(debug=True)