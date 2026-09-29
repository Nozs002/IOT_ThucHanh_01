"""Bài 3 - Mô phỏng thiết bị đèn thông minh."""

from __future__ import annotations

import json

import paho.mqtt.client as mqtt

from mqtt_config import connect_client, create_client

DEVICE_ID = "light01"
COMMAND_TOPIC = f"iot/lab/{DEVICE_ID}/cmd"
STATUS_TOPIC = f"iot/lab/{DEVICE_ID}/status"
VALID_COMMANDS = {"ON", "OFF"}

light_status = "OFF"


def publish_status(client: mqtt.Client) -> None:
    payload = json.dumps(
        {"device_id": DEVICE_ID, "status": light_status},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    result = client.publish(STATUS_TOPIC, payload, qos=1, retain=True)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Da gui trang thai: {payload}")
    else:
        print(f"Gui trang thai that bai, ma loi: {result.rc}")


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
    client.subscribe(COMMAND_TOPIC, qos=1)
    print(f"Dang cho lenh tren topic: {COMMAND_TOPIC}")
    publish_status(client)


def on_message(
    client: mqtt.Client, userdata: object, message: mqtt.MQTTMessage
) -> None:
    global light_status

    try:
        command = message.payload.decode("utf-8").strip().upper()
    except UnicodeDecodeError:
        print("Lenh khong phai chuoi UTF-8 hop le")
        return

    print(f"\nNhan lenh: {command}")
    if command not in VALID_COMMANDS:
        print("Lenh khong hop le. Chi chap nhan ON hoac OFF.")
        return

    light_status = command
    print(f"Den da chuyen sang trang thai {light_status}")
    publish_status(client)


def main() -> None:
    client = create_client("device-light01-bai3")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        connect_client(client)
        print("Nhan Ctrl+C de dung thiet bi")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDa dung Smart Light Device")
    except OSError as exc:
        print(f"Khong the ket noi MQTT broker: {exc}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
