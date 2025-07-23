import os
import glob
import time
from collections import namedtuple
from dotenv import load_dotenv

SensorReading = namedtuple("SensorReading", ["temperature", "humidity"])


class DS18B20Sensor:
    def __init__(self, sensor_id: str = None):
        self.base_dir = "/sys/bus/w1/devices/"

        if sensor_id:
            self.device_folder = os.path.join(self.base_dir, sensor_id)
        else:
            try:
                self.device_folder = glob.glob(self.base_dir + "28*")[0]
            except IndexError:
                raise FileNotFoundError("No DS18B20 sensor found. Check wiring and w1 modules.")

        self.device_file = os.path.join(self.device_folder, "w1_slave")

        # Warm-up read
        _ = self._read_raw()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # No cleanup needed for DS18B20, but it's here for consistency
        pass

    def _read_raw(self):
        with open(self.device_file, "r") as f:
            return f.readlines()

    def _parse_temperature(self):
        lines = self._read_raw()
        retry_count = 5
        while lines[0].strip()[-3:] != "YES" and retry_count > 0:
            time.sleep(0.2)
            lines = self._read_raw()
            retry_count -= 1

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            try:
                return float(temp_string) / 1000.0
            except ValueError:
                print("[DS18B20 ERROR] Could not parse temperature value.")

        return None

    def read(self):
        for attempt in range(3):
            temp_c = self._parse_temperature()
            if temp_c is not None:
                return SensorReading(temperature=temp_c, humidity=None)
            print(f"[DS18B20 WARNING] Attempt {attempt + 1}: Failed to get temperature")
            time.sleep(1)

        print("[DS18B20 ERROR] Failed to read temperature after 3 attempts.")
        return SensorReading(temperature=None, humidity=None)


if __name__ == "__main__":
    load_dotenv()

    sensor_id = os.getenv("DS18B20_ID")
    with DS18B20Sensor(sensor_id=sensor_id) as sensor:
        reading = sensor.read()

        if reading.temperature is not None:
            print(f"DS18B20 Temp: {reading.temperature:.2f} C")
        else:
            print("Failed to read from DS18B20 sensor.")
