"""Cấu hình MQTT dùng chung cho các chương trình thực hành."""

from __future__ import annotations

import os
import ssl

import paho.mqtt.client as mqtt


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default))
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Bien moi truong {name} phai la so nguyen") from exc


MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = _read_int("MQTT_PORT", 1883)
MQTT_KEEPALIVE = _read_int("MQTT_KEEPALIVE", 60)
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def create_client(client_id: str) -> mqtt.Client:
    """Tạo MQTT client theo cấu hình lấy từ biến môi trường."""
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
        protocol=mqtt.MQTTv311,
    )

    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    if MQTT_USE_TLS:
        client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

    return client


def connect_client(client: mqtt.Client) -> None:
    """Kết nối client tới broker đã cấu hình."""
    print(f"Dang ket noi MQTT broker {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
