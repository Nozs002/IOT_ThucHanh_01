"""Bài 1 - Nhận và hiển thị thông điệp MQTT."""

from __future__ import annotations

from datetime import datetime

import paho.mqtt.client as mqtt

from mqtt_config import connect_client, create_client

TOPIC = "iot/lab/message"


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
    print(f"Dang lang nghe topic: {TOPIC}")


def on_message(
    client: mqtt.Client, userdata: object, message: mqtt.MQTTMessage
) -> None:
    try:
        payload = message.payload.decode("utf-8")
    except UnicodeDecodeError:
        payload = repr(message.payload)

    print("\nNhan duoc message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {payload}")
    print(f"Time: {datetime.now():%H:%M:%S}")


def main() -> None:
    client = create_client("subscriber-bai1")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        connect_client(client)
        print("Nhan Ctrl+C de dung chuong trinh")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDa dung Subscriber")
    except OSError as exc:
        print(f"Khong the ket noi MQTT broker: {exc}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
