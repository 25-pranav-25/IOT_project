# === UPDATED app.py ===

from flask import Flask, jsonify, render_template, request
import paho.mqtt.client as mqtt
import json, joblib, os
import numpy as np
import pandas as pd

app = Flask(__name__)

building_map = {
    1: "Barak", 2: "Brahmaputra", 3: "Kameng", 4: "Umiam", 5: "Manas",
    6: "Dihing", 7: "Lohit", 8: "Siang", 9: "Gourang", 10: "Kapili",
    11: "Disang", 12: "Dhansiri", 13: "Subhansiri", 14: "Core1", 15: "Core2",
    16: "Core3", 17: "Core4", 18: "Core5", 19: "Library", 20: "Admin"
}

models, scalers = {}, {}
for i in range(1, 21):
    model_path = f"models/rf_model_building_{i}.pkl"
    scaler_path = f"scalers/scaler_building_{i}.pkl"
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        models[i] = joblib.load(model_path)
        scalers[i] = joblib.load(scaler_path)

all_data = pd.DataFrame(columns=["building_id", "meter_reading", "time", "month", "day", "weekend", "prediction"])

MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensor/data"

def on_message(client, userdata, msg):
    global all_data
    try:
        data = json.loads(msg.payload.decode())
        building_id = data["building_id"]
        model, scaler = models.get(building_id), scalers.get(building_id)

        if model and scaler:
            raw = np.array([[data["meter_reading"], data["time"], data["month"], data["day"], data["weekend"]]])
            input_scaled = scaler.transform(raw)
            prediction = int(model.predict(input_scaled)[0])
            data["prediction"] = prediction
            all_data = pd.concat([all_data, pd.DataFrame([data])], ignore_index=True)
        else:
            print(f"No model for building {building_id}")
    except Exception as e:
        print("MQTT error:", e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

@app.route("/")
def index():
    return render_template("index.html", building_map=building_map)

@app.route("/data/<int:building_id>")
def building_data(building_id):
    data = all_data[all_data["building_id"] == building_id].copy()
    data = data.to_dict(orient="records")
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
