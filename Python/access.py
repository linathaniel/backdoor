import socket
from getpass import getpass

SERVER_IP = '127.0.0.1'
SERVER_PORT = 4444

def connect_to_server():
    client = socket.socket()
    print("[CLIENT] Connecting to server...")
    client.connect((SERVER_IP, SERVER_PORT))
    print("[CLIENT] Connected.")

    password = getpass("Enter password: ")
    client.send(password.encode())

    try:
        response = client.recv(1024).decode().strip()
        print(f"[CLIENT DEBUG] Server responded with: '{response}'")
    except Exception as e:
        print(f"[CLIENT ERROR] Failed to receive response: {e}")
        client.close()
        return

    if response == "success":
        print("[CLIENT] Login Successful!\n")
    else:
        print("[CLIENT] Login Failed!")
        client.close()
        return

    while True:
        cmd = input(">>> ")
        if cmd.lower() == "exit":
            client.send(cmd.encode())
            break

        if cmd.strip() == "":
            continue

        client.send(cmd.encode())
        result = client.recv(4096).decode()
        print(result)

    client.close()
    print("[CLIENT] Connection closed.")

if __name__ == "__main__":
    connect_to_server()