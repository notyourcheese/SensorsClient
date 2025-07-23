import os
from . import dht11, dht22, ds18b20

SENSOR_TYPE = os.getenv("SENSOR_TYPE", "DHT22").upper()

sensor_class_map = {
    "DHT11": dht11.DHT11Sensor,
    "DHT22": dht22.DHT22Sensor,
    "DS18B20": ds18b20.DS18B20Sensor,
}

if SENSOR_TYPE not in sensor_class_map:
    raise ValueError(f"Unsupported sensor type: {SENSOR_TYPE}")

sensor = sensor_class_map[SENSOR_TYPE]
