import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    """Server se aane wale messages ko background mein print karta hai."""
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\nServer ne connection band kar diya.")
                break
            print(f"\nServer: {data.decode()}")
        except (ConnectionResetError, OSError):
            print("\nServer se connection toot gaya.")
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Server se connect nahi ho saka. Pehle server.py chalayein.")
        return

    print(f"Server ({HOST}:{PORT}) se connect ho gaya.")
    print("Message likhein. Bahar nikalne ke liye 'exit' likhein.\n")

    receiver = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    receiver.start()

    try:
        while True:
            message = input("You: ").strip()
            if not message:
                continue

            client.sendall(message.encode())

            if message.lower() == "exit":
                break
    except (KeyboardInterrupt, EOFError):
        print("\nClient band ho raha hai.")
    finally:
        client.close()
        print("Connection closed.")


if __name__ == "__main__":
    start_client()
