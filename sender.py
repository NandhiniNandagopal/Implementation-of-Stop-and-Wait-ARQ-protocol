import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(3)

client.connect((HOST, PORT))

print("STOP-AND-WAIT ARQ SENDER")

# User input
n = int(input("\nEnter number of frames: "))

frames = []

for i in range(n):
    data = input(f"Enter data for Frame {i}: ")
    frames.append(data)

print("\nStarting transmission...\n")

for i in range(n):

    while True:
        print(f"Sender: Sending Frame {i}")
        print(f"Sender: Data = {frames[i]}")

        client.send(f"{i}|{frames[i]}".encode())

        try:
            ack = client.recv(1024).decode()

            if ack == str(i):
                print(f"Sender: ACK {ack} received")
                print(f"Frame {i} successfully transmitted.\n")
                break

        except socket.timeout:
            print(f"Timeout! ACK for Frame {i} not received.")
            print(f"Retransmitting Frame {i}...\n")

client.send("END".encode())

print("All frames transmitted successfully!")

client.close()