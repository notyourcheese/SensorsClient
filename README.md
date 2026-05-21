# SensorsClient

Lightweight Python client for collecting hardware sensor data and pushing readings to a remote API.

Designed for Raspberry Pi / edge devices using temperature and humidity sensors such as:

- DHT11
- DHT22
- DS18B20

The client:

- Loads configured sensors from environment variables
- Registers the device with the API
- Collects sensor readings
- Sends readings to a backend service over HTTP

---

## Features

- Multi-sensor support
- Automatic device registration
- Sensor autodiscovery via config
- Hostname + local IP reporting
- Simple `.env` configuration
- Easy deployment on small Linux devices

---

## Project Structure

```text
.
├── Makefile
├── requirements.txt
└── src
    ├── main.py
    ├── sensors
    └── test_sensors.py
```

---

## Requirements

- Python 3.10+
- Linux device with GPIO support (recommended)
- Supported sensor hardware

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```env
API_URL=http://localhost:8811
API_TOKEN=your-api-token

DEVICE_NAME=living-room-pi
DEVICE_LOCATION=Living Room

SENSOR_TYPES=DHT22

DHT22_PIN=4
```

### Supported Sensor Types

| Sensor | Notes |
|---|---|
| `DHT11` | Temperature + humidity |
| `DHT22` | Higher precision temp/humidity |
| `DS18B20` | Temperature only |

You can configure multiple sensors:

```env
SENSOR_TYPES=DHT22,DS18B20
```

---

## Running

```bash
python src/main.py
```

The client will:

1. Load configured sensors
2. Register the device with the API
3. Read sensor values
4. Send readings to the backend

---

## Example Payload

### Device Registration

```json
{
  "device_name": "living-room-pi",
  "location": "Living Room",
  "sensors": [
    {
      "sensor_type": "DHT22",
      "model": "DHT22Sensor",
      "pin": 4,
      "unique_id": "living-room-pi-dht22"
    }
  ]
}
```

### Sensor Reading

```json
{
  "readings": [
    {
      "sensor_unique_id": "living-room-pi-dht22",
      "temperature": 22.5,
      "humidity": 48.2,
      "timestamp": "2026-05-22T10:00:00Z",
      "hostname": "raspberrypi",
      "ip_address": "192.168.1.10"
    }
  ]
}
```

---

## Development

Run tests:

```bash
python -m pytest src/test_sensors.py
```

---

## Notes

- The client expects a compatible backend API.
- Sensor registration occurs on every startup.
- Invalid sensor readings are skipped automatically.

---

## License

MIT
