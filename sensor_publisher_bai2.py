"""Bài 2 - Mô phỏng cảm biến nhiệt độ và độ ẩm."""

from __future__ import annotations

import json
import random
import time

from mqtt_config import connect_client, create_client

DEVICE_ID = "sensor01"
TOPIC = f"iot/lab/{DEVICE_ID}/data"
PUBLISH_INTERVAL = 3


def create_sensor_data() -> dict[str, str | float]:
    return {
        "device_id": DEVICE_ID,
        "temperature": round(random.uniform(20.0, 40.0), 1),
        "humidity": round(random.uniform(30.0, 90.0), 1),
    }


def main() -> None:
    client = create_client("sensor-publisher-bai2")

    try:
        connect_client(client)
        client.loop_start()
        print(f"Gui du lieu moi {PUBLISH_INTERVAL} giay. Nhan Ctrl+C de dung.")

        while True:
            data = create_sensor_data()
            payload = json.dumps(data, ensure_ascii=False)
            result = client.publish(TOPIC, payload, qos=1)
            result.wait_for_publish()

            if result.rc != 0:
                print(f"Gui du lieu that bai, ma loi: {result.rc}")
            else:
                print(f"\nTopic: {TOPIC}")
                print(f"Payload: {payload}")

            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        print("\nDa dung Sensor Publisher")
    except OSError as exc:
        print(f"Khong the ket noi MQTT broker: {exc}")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
