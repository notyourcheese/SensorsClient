import os
import time
import requests
from dotenv import load_dotenv
from sensors import sensor_class_map

load_dotenv()
API_URL = os.getenv("API_URL", "http://10.10.10.6:8811")  # or localhost if running locally

def load_sensors():
    sensor_types = os.getenv("SENSOR_TYPES", "DHT22").upper().split(",")
    sensors = []

    for sensor_type in sensor_types:
        sensor_type = sensor_type.strip()
        cls = sensor_class_map.get(sensor_type)
        if not cls:
            raise ValueError(f"Unsupported SENSOR_TYPE '{sensor_type}'")

        if sensor_type in ("DHT11", "DHT22"):
            sensor = cls(f"{sensor_type}_PIN")
        elif sensor_type == "DS18B20":
            sensor = cls()
        else:
            raise ValueError(f"Unsupported SENSOR_TYPE '{sensor_type}'")

        sensors.append((sensor_type, sensor))
    return sensors

def register_device(device_name, location, sensors):
    payload = {
        "device_name": device_name,
        "location": location,
        "sensors": []
    }

    for sensor_type, sensor in sensors:
        payload["sensors"].append({
            "sensor_type": sensor_type,
            "model": sensor.__class__.__name__,
            "pin": getattr(sensor, 'pin', None),
            "unique_id": f"{device_name.lower()}-{sensor_type.lower()}"
        })

    try:
        r = requests.post(f"{API_URL}/sensors/register", json=payload)
        r.raise_for_status()
        print("[✓] Registration successful.")
    except Exception as e:
        print(f"[!] Registration failed: {e}")

def post_readings(device_name, sensors):
    readings = []

    for sensor_type, sensor in sensors:
        reading = sensor.read()
        if reading.temperature is not None:
            readings.append({
                "sensor_unique_id": f"{device_name.lower()}-{sensor_type.lower()}",
                "temperature": reading.temperature,
                "humidity": reading.humidity,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })

    if not readings:
        print("[!] No valid readings to send.")
        return

    try:
        r = requests.post(f"{API_URL}/readings/", json={"readings": readings})
        r.raise_for_status()
        print(f"[✓] Sent {len(readings)} reading(s).")
    except Exception as e:
        print(f"[!] Failed to send readings: {e}")

def main():


    device_name = os.getenv("DEVICE_NAME")
    location = os.getenv("DEVICE_LOCATION")

    if not device_name or not location:
        raise EnvironmentError("DEVICE_NAME and DEVICE_LOCATION must be set in .env")

    sensors = load_sensors()
    register_device(device_name, location, sensors)
    post_readings(device_name, sensors)

if __name__ == "__main__":
    main()
