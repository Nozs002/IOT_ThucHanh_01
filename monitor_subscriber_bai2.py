"""Bài 2 - Theo dõi dữ liệu cảm biến và phát cảnh báo."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import paho.mqtt.client as mqtt

from mqtt_config import connect_client, create_client

TOPIC = "iot/lab/sensor01/data"
HIGH_TEMPERATURE = 35.0
LOW_HUMIDITY = 40.0


def parse_sensor_payload(payload: bytes) -> dict[str, Any]:
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Payload JSON phai la mot object")

    required_fields = {"device_id", "temperature", "humidity"}
    missing_fields = required_fields - data.keys()
    if missing_fields:
        raise ValueError(f"Thieu truong: {', '.join(sorted(missing_fields))}")

    data["temperature"] = float(data["temperature"])
    data["humidity"] = float(data["humidity"])
    return data


def on_connect(
    client: mqtt.Client,
    userdata: object,
    flags: mqtt.ConnectFlags,
    reason_code: mqtt.ReasonCode,
    properties: mqtt.Properties | None,
) -> None:
    if reason_code.is_failure:
        print(f"Ket noi that bai: {reason_code}")
        return

    print("Da ket noi MQTT broker")
    client.subscribe(TOPIC, qos=1)
    print(f"Dang theo doi topic: {TOPIC}")


def on_message(
    client: mqtt.Client, userdata: object, message: mqtt.MQTTMessage
) -> None:
    try:
        data = parse_sensor_payload(message.payload)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"\nPayload khong hop le tren topic {message.topic}: {exc}")
        return

    temperature = data["temperature"]
    humidity = data["humidity"]

    print(f"\nTime: {datetime.now():%H:%M:%S}")
    print(f"Device: {data['device_id']}")
    print(f"Temperature: {temperature:.1f} C")
    print(f"Humidity: {humidity:.1f} %")

    if temperature > HIGH_TEMPERATURE:
        print("CANH BAO: Nhiet do cao")
    if humidity < LOW_HUMIDITY:
        print("CANH BAO: Do am thap")


def main() -> None:
    client = create_client("monitor-subscriber-bai2")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        connect_client(client)
        print("Nhan Ctrl+C de dung chuong trinh")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDa dung Monitoring Subscriber")
    except OSError as exc:
        print(f"Khong the ket noi MQTT broker: {exc}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
