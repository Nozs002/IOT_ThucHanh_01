"""Bài 1 - Gửi thông điệp cơ bản lên MQTT."""

from __future__ import annotations

import argparse
import time

from mqtt_config import connect_client, create_client

TOPIC = "iot/lab/message"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MQTT Publisher cho bai 1")
    parser.add_argument("--name", default="Phạm Hồng Sơn", help="Ho ten sinh vien")
    parser.add_argument("--student-id", default="B23DCCN723", help="Ma sinh vien")
    parser.add_argument(
        "--message",
        default="Xin chao tu client Python MQTT",
        help="Noi dung thong diep",
    )
    parser.add_argument("--count", type=int, default=1, help="So thong diep can gui")
    parser.add_argument(
        "--interval", type=float, default=1.0, help="Khoang cach giua cac lan gui"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.count < 1:
        raise ValueError("--count phai lon hon hoac bang 1")
    if args.interval < 0:
        raise ValueError("--interval khong duoc am")

    client = create_client("publisher-bai1")

    try:
        connect_client(client)
        client.loop_start()

        payload = f"{args.message} - {args.student_id} - {args.name}"
        for index in range(args.count):
            result = client.publish(TOPIC, payload, qos=1)
            result.wait_for_publish()
            if result.rc != 0:
                raise RuntimeError(f"Publish that bai, ma loi: {result.rc}")

            print(f"Da gui ({index + 1}/{args.count})")
            print(f"Topic: {TOPIC}")
            print(f"Payload: {payload}")

            if index < args.count - 1:
                time.sleep(args.interval)
    except OSError as exc:
        print(f"Khong the ket noi MQTT broker: {exc}")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
