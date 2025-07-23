"""
based on the DS18B20 (ky-004) temperature sensor and code from joyit,
The temperature evaluation: On the Raspberry Pi, detected one-Wire slaves are assigned to a separate subfolder in the folder
/sys/bus/w1/devices/ are assigned to an own subfolder. In this folder is the file w1-slave
in which the data sent over the one-wire bus is stored.
"""

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
        _ = self._read_raw()  # warm-up read

    def _read_raw(self):
        with open(self.device_file, "r") as f:
            return f.readlines()

    def _parse_temperature(self):
        lines = self._read_raw()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self._read_raw()

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            return float(temp_string) / 1000.0

        return None

    def read(self):
        temp_c = self._parse_temperature()
        return SensorReading(temperature=temp_c, humidity=None)


if __name__ == "__main__":
    load_dotenv()

    sensor_id = os.getenv("DS18B20_ID")
    sensor = DS18B20Sensor(sensor_id=sensor_id)

    reading = sensor.read()
    if reading.temperature is not None:
        print(f"DS18B20 Temp: {reading.temperature:.2f}°C")
    else:
        print("Failed to read from DS18B20 sensor.")
