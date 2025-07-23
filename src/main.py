from sensors import sensor_class_map
from dotenv import load_dotenv
import os
import board

def resolve_pin(var_name):
    pin_name = os.getenv(var_name)
    if not pin_name:
        raise EnvironmentError(f"{var_name} not set in .env")
    try:
        return getattr(board, pin_name)
    except AttributeError:
        raise ValueError(f"Invalid pin name '{pin_name}' for {var_name}")

def main():
    load_dotenv()

    sensor_types = os.getenv("SENSOR_TYPES", "DHT22").upper().split(",")
    sensors = []

    for sensor_type in sensor_types:
        sensor_type = sensor_type.strip()
        cls = sensor_class_map.get(sensor_type)
        if not cls:
            raise ValueError(f"Unsupported SENSOR_TYPE '{sensor_type}'")

        if sensor_type in ("DHT11", "DHT22"):
            pin = resolve_pin(f"{sensor_type}_PIN")
            sensors.append((sensor_type, cls(pin)))
        elif sensor_type == "DS18B20":
            sensor_id = os.getenv("DS18B20_ID")  # optional
            sensors.append((sensor_type, cls(sensor_id)))
        else:
            raise ValueError(f"Unsupported SENSOR_TYPE '{sensor_type}'")

    for name, sensor in sensors:
        reading = sensor.read()
        if reading.temperature is not None:
            print(f"[{name}] Temp: {reading.temperature:.2f}°C", end="")
            if reading.humidity is not None:
                print(f", Humidity: {reading.humidity:.2f}%")
            else:
                print()
        else:
            print(f"[{name}] Failed to read sensor data.")


if __name__ == "__main__":
    main()
