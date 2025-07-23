import adafruit_dht
from collections import namedtuple
from .utils import get_board_pin
import time

SensorReading = namedtuple("SensorReading", ["temperature", "humidity"])


class DHT11Sensor:
    def __init__(self, env_var_name: str = "DHT11_PIN"):
        pin = get_board_pin(env_var_name)
        self.dht_device = adafruit_dht.DHT11(pin)

    def read(self):
        for _ in range(3):  # up to 3 tries
            try:
                temperature_c = self.dht_device.temperature
                humidity = self.dht_device.humidity
                return SensorReading(temperature=temperature_c, humidity=humidity)
            except RuntimeError as err:
                print(f"[DHT22 ERROR] {err.args[0]}")
                time.sleep(1)
        return SensorReading(temperature=None, humidity=None)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    sensor = DHT11Sensor()  # Uses default "DHT11_PIN"
    reading = sensor.read()

    if reading.temperature is not None:
        print(f"Temperature: {reading.temperature:.1f}°C, Humidity: {reading.humidity:.1f}%")
    else:
        print("Failed to read from DHT11 sensor.")
