import network
import time
import ujson
import random
from umqtt.simple import MQTTClient

# === WiFi & MQTT Config ===
WIFI_SSID = 'Pranav'
WIFI_PASSWORD = '12121212'
MQTT_BROKER = 'YOUR_IP'
MQTT_PORT = 1883
MQTT_TOPIC = b'sensor/data'

# === Building usage categories ===
very_high_usage = [18, 19, 20, 2, 7]
high_usage = [2, 7, 11, 14, 15, 16, 17]
medium_usage = [1, 3, 4, 9, 12, 13]

low_usage = []
for i in range(1, 21):
    if i not in (very_high_usage + high_usage + medium_usage):
        low_usage.append(i)

# === Helper functions ===
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("WiFi connected:", wlan.ifconfig())

def normalvariate(mu, sigma):
    import math
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mu + z0 * sigma

def get_category(building_id):
    if building_id in very_high_usage:
        return "very_high", 300, 40
    elif building_id in high_usage:
        return "high", 230, 30
    elif building_id in medium_usage:
        return "medium", 150, 20
    else:
        return "low", 100, 10

def generate_reading(building_id, is_weekend):
    category, mean, std = get_category(building_id)

    # Weekend multiplier
    if building_id <= 13:  # Hostels
        if is_weekend:
            mean *= 1.2
    else:  # Academic/Admin
        if is_weekend:
            mean *= 0.7

    reading = normalvariate(mean, std)
    return max(0, round(reading, 2))



# === Main loop ===
def main():
    connect_wifi()
    client = MQTTClient("esp32", MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("MQTT connected")

    for day in range(1, 3):  # April 1 to 10
        for hour in range(24):
            weekday = ((day - 1) % 7)  # simulate day-of-week
            is_weekend = 1 if weekday >= 5 else 0

            for building_id in range(1, 21):
                reading = generate_reading(building_id, is_weekend)
                payload = {
                    'building_id': building_id,
                    'meter_reading': reading,
                    'time': hour,
                    'month': 4,
                    'day': weekday + 1,
                    'weekend': is_weekend
                }

                client.publish(MQTT_TOPIC, ujson.dumps(payload))
                print("Published:", payload)
                time.sleep(0.05)  # avoid flooding

    client.disconnect()
    print("All data sent.")

main()
