"""Bài 3 - Ứng dụng gửi lệnh và nhận trạng thái đèn."""

from __future__ import annotations

import json
import threading

import paho.mqtt.client as mqtt

from mqtt_config import connect_client, create_client

DEVICE_ID = "light01"
COMMAND_TOPIC = f"iot/lab/{DEVICE_ID}/cmd"
STATUS_TOPIC = f"iot/lab/{DEVICE_ID}/status"
VALID_COMMANDS = {"ON", "OFF"}

connected_event = threading.Event()


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

    client.subscribe(STATUS_TOPIC, qos=1)
    connected_event.set()
    print(f"Da ket noi va dang lang nghe: {STATUS_TOPIC}")


def on_message(
    client: mqtt.Client, userdata: object, message: mqtt.MQTTMessage
) -> None:
    try:
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("Payload JSON phai la mot object")
        if "device_id" not in data or "status" not in data:
            raise ValueError("Payload thieu device_id hoac status")
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"\nTrang thai khong hop le: {exc}")
        return

    print("\nTrang thai nhan duoc:")
    print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))


def main() -> None:
    client = create_client("controller-bai3")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        connect_client(client)
        client.loop_start()

        if not connected_event.wait(timeout=10):
            print("Khong nhan duoc xac nhan ket noi trong 10 giay")
            return

        print("Nhap ON/OFF de dieu khien den, hoac EXIT de ket thuc.")
        while True:
            command = input("\nNhap lenh: ").strip().upper()

            if command == "EXIT":
                break
            if command not in VALID_COMMANDS:
                print("Lenh khong hop le. Vui long nhap ON, OFF hoac EXIT.")
                continue

            result = client.publish(COMMAND_TOPIC, command, qos=1)
            result.wait_for_publish()
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Da gui lenh {command} toi {DEVICE_ID}")
            else:
                print(f"Gui lenh that bai, ma loi: {result.rc}")
    except (KeyboardInterrupt, EOFError):
        print("\nDa dung Controller App")
    except OSError as exc:
        print(f"Khong the ket noi MQTT broker: {exc}")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
