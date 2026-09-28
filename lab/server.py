import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

print_lock = threading.Lock()
clients = set()
clients_lock = threading.Lock()


def safe_print(message):
    """Print ko thread-safe banata hai."""
    with print_lock:
        print(message)


def add_client(conn):
    with clients_lock:
        clients.add(conn)


def remove_client(conn):
    with clients_lock:
        clients.discard(conn)


def broadcast(message, sender_conn=None):
    with clients_lock:
        recipients = list(clients)

    for conn in recipients:
        if conn is sender_conn:
            continue
        try:
            conn.sendall(message.encode())
        except (BrokenPipeError, OSError):
            remove_client(conn)
            conn.close()


def handle_client(conn, addr):
    """Har client ke liye alag thread."""
    thread_name = threading.current_thread().name
    client_ip, client_port = addr

    add_client(conn)
    safe_print(f"[CONNECTED]  Thread: {thread_name} | IP: {client_ip} | "
               f"Port: {client_port} | Active Clients: {len(clients)}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            safe_print(f"[RECEIVED]   Thread: {thread_name} | IP: {client_ip} | "
                       f"Port: {client_port} | Message: {message}")

            if message.lower() == "exit":
                conn.sendall("Goodbye! Connection closing.".encode())
                break

            broadcast(f"[{client_ip}:{client_port}] says: {message}", sender_conn=conn)
    except ConnectionResetError:
        safe_print(f"[ERROR]      Thread: {thread_name} | Client {client_ip}:{client_port} "
                   f"achanak disconnect ho gaya.")
    finally:
        remove_client(conn)
        conn.close()
        safe_print(f"[DISCONNECT] Thread: {thread_name} | IP: {client_ip} | "
                   f"Port: {client_port} | Active Clients: {len(clients)}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    safe_print(f"[STARTED]    Server {HOST}:{PORT} par sun raha hai... (Band karne ke liye Ctrl+C)")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        safe_print("\n[SHUTDOWN]   Server band ho raha hai.")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
