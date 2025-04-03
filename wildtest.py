import socket

# Set the IP and port of the measurement PC
server_ip = "192.168.1.144"  # Replace with actual measurement PC IP
server_port = 2055  # Replace with the actual port number

# Create a socket to receive data
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))

print("Connected! Listening for data...")

try:
    while True:
        data = sock.recv(1024)  # Receive data in chunks
        if not data:
            break  # Stop if no data received
        print(data.decode())  # Decode and print data
except KeyboardInterrupt:
    print("Closing connection.")
    sock.close()
