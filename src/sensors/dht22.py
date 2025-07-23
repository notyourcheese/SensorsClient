# import adafruit_dht
from collections import namedtuple
import time
from .utils import get_board_pin

SensorReading = namedtuple("SensorReading", ["temperature", "humidity"])


class DHT22Sensor:
    def __init__(self, env_var_name: str = "DHT22_PIN"):
        import adafruit_dht
        pin = get_board_pin(env_var_name)
        self.dht_device = adafruit_dht.DHT22(pin)

    def read(self):
        for attempt in range(3):
            try:
                temperature = self.dht_device.temperature
                humidity = self.dht_device.humidity

                # Only return if both are non-None
                if temperature is not None and humidity is not None:
                    return SensorReading(temperature=temperature, humidity=humidity)

                print(f"[DHT22 WARNING] Got None values on attempt {attempt + 1}")
            except RuntimeError as err:
                print(f"[DHT22 ERROR] Attempt {attempt + 1}: {err}")
            time.sleep(2)

        print("[DHT22 ERROR] Failed to read after 3 attempts.")
        return SensorReading(temperature=None, humidity=None)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    sensor = DHT22Sensor()  # Uses default "DHT22_PIN"
    reading = sensor.read()

    if reading.temperature is not None:
        print(f"Temperature: {reading.temperature:.1f} C, Humidity: {reading.humidity:.1f}%")
    else:
        print("Failed to read from DHT22 sensor.")
