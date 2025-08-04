from sensors import sensor_class_map
from dotenv import load_dotenv
import os
import board


def main():
    load_dotenv()

    sensor_types = os.getenv("SENSOR_TYPES", "DHT22").upper().split(",")

    for sensor_type in sensor_types:
        sensor_type = sensor_type.strip()
        cls = sensor_class_map.get(sensor_type)
        if not cls:
            raise ValueError(f"Unsupported SENSOR_TYPE '{sensor_type}'")

        print(f"Reading from {sensor_type}...")

        if sensor_type in ("DHT11", "DHT22"):
            with cls(f"{sensor_type}_PIN") as sensor:
                reading = sensor.read()
        elif sensor_type == "DS18B20":
            with cls() as sensor:
                reading = sensor.read()
        else:
            raise ValueError(f"Unsupported SENSOR_TYPE '{sensor_type}'")

        if reading.temperature is not None:
            print(f"[{sensor_type}] Temp: {reading.temperature:.2f} C", end="")
            if reading.humidity is not None:
                print(f", Humidity: {reading.humidity:.2f}%")
            else:
                print()
        else:
            print(f"[{sensor_type}] Failed to read sensor data.")


if __name__ == "__main__":
    main()
