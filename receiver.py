import socket
import random

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Receiver started...")
print("Waiting for sender connection...")

conn, address = server.accept()
print("Sender connected:", address)

expected_frame = 0

while True:
    data = conn.recv(1024).decode()

    if not data:
        break

    if data == "END":
        print("\nAll frames received.")
        break

    frame = int(data)

    print(f"\nReceiver: Frame {frame} received")

    if random.random() < 0.2:
        print(f"Receiver: Frame {frame} discarded")
        continue

    if frame == expected_frame:
        print(f"Receiver: Frame {frame} accepted")
        print(f"Receiver: Sending ACK {frame}")

        conn.send(str(frame).encode())

        expected_frame += 1
    else:
        print("Receiver: Duplicate frame")
        print(f"Receiver: Sending ACK {expected_frame - 1}")

        conn.send(str(expected_frame - 1).encode())

conn.close()
server.close()

print("Receiver stopped.")
