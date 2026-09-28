lab
# TCP Lab 3 – Multithreaded Client-Server Chat

A simple **TCP client-server application in Python** using the `socket` and `threading` modules. The server handles **multiple clients at the same time**, with one thread per client, and uses a **lock** to keep shared data and terminal output safe.

---

## Features

- Multithreaded TCP server (a new thread is created for every client)
- Multiple clients can connect and chat with the server simultaneously
- `threading.Lock` used to:
  - prevent mixed-up output from different threads
  - safely update the shared `active_clients` counter (avoids race conditions)
- Live logging on the server: connect, receive, disconnect, active client count
- Graceful handling of `exit`, sudden disconnects and `Ctrl+C`
- Client shows a clear message if the server is not running

---

## Project Structure

```
tcp_lab3/
├── server.py        # Multithreaded TCP server
├── client.py        # TCP client
├── screenshots/     # Terminal output screenshots
│   ├── 1_server_terminal.png
│   ├── 2_client1_terminal.png
│   └── 3_client2_terminal.png
└── README.md
```

---

## Requirements

- Python 3.8 or higher
- No external libraries needed (only the standard library)

---

## How to Run

Open **three terminals** (in VS Code: `Terminal > New Terminal`, then use the split button).

**Terminal 1 – start the server**
```bash
python server.py
```

**Terminal 2 – start client 1**
```bash
python client.py
```

**Terminal 3 – start client 2**
```bash
python client.py
```

Type a message in any client and press Enter. Type `exit` to disconnect.
Press `Ctrl+C` in the server terminal to stop the server.

> Always start `server.py` **before** the clients.

---

## How It Works

### Server (`server.py`)

| Part | Purpose |
|------|---------|
| `start_server()` | Creates the socket, binds to `127.0.0.1:5000`, and accepts connections in a loop. Each client gets its own `Thread`. |
| `handle_client()` | Runs in a separate thread per client. Receives messages, sends replies, and closes the connection on `exit`. |
| `safe_print()` | Prints with a lock so output from multiple threads does not get mixed. |
| `update_client_count()` | Updates the shared `active_clients` counter under a lock. |

### Client (`client.py`)

1. Connects to `127.0.0.1:5000`
2. Reads a message from the user and sends it
3. Prints the server's reply
4. Stops when the user types `exit`

---

## Sample Output

### Server
```
[STARTED]    Server 127.0.0.1:5000 par sun raha hai... (Band karne ke liye Ctrl+C)
[CONNECTED]  Thread: Thread-1 (handle_client) | IP: 127.0.0.1 | Port: 42842 | Active Clients: 1
[CONNECTED]  Thread: Thread-2 (handle_client) | IP: 127.0.0.1 | Port: 42844 | Active Clients: 2
[RECEIVED]   Thread: Thread-1 (handle_client) | IP: 127.0.0.1 | Port: 42842 | Message: Hello Server
[RECEIVED]   Thread: Thread-2 (handle_client) | IP: 127.0.0.1 | Port: 42844 | Message: Salam, main Client 2 hoon
[RECEIVED]   Thread: Thread-1 (handle_client) | IP: 127.0.0.1 | Port: 42842 | Message: TCP multithreading test
[RECEIVED]   Thread: Thread-2 (handle_client) | IP: 127.0.0.1 | Port: 42844 | Message: exit
[DISCONNECT] Thread: Thread-2 (handle_client) | IP: 127.0.0.1 | Port: 42844 | Active Clients: 1
[RECEIVED]   Thread: Thread-1 (handle_client) | IP: 127.0.0.1 | Port: 42842 | Message: exit
[DISCONNECT] Thread: Thread-1 (handle_client) | IP: 127.0.0.1 | Port: 42842 | Active Clients: 0
^C
[SHUTDOWN]   Server band ho raha hai.
```

### Client 1
```
Server (127.0.0.1:5000) se connect ho gaya.
Message likhein. Bahar nikalne ke liye 'exit' likhein.

You: Hello Server
Server: Server (Thread-1 (handle_client)) ne receive kiya: Hello Server
You: TCP multithreading test
Server: Server (Thread-1 (handle_client)) ne receive kiya: TCP multithreading test
You: exit
Server: Goodbye! Connection closing.
Connection closed.
```

### Client 2
```
Server (127.0.0.1:5000) se connect ho gaya.
Message likhein. Bahar nikalne ke liye 'exit' likhein.

You: Salam, main Client 2 hoon
Server: Server (Thread-2 (handle_client)) ne receive kiya: Salam, main Client 2 hoon
You: exit
Server: Goodbye! Connection closing.
Connection closed.
```

### Screenshots

**Server**

![Server terminal](screenshots/1_server_terminal.png)

**Client 1**

![Client 1 terminal](screenshots/2_client1_terminal.png)

**Client 2**

![Client 2 terminal](screenshots/3_client2_terminal.png)

---

## Concepts Covered

- TCP sockets (`socket.AF_INET`, `socket.SOCK_STREAM`)
- `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`
- Multithreading with `threading.Thread`
- Thread synchronization with `threading.Lock`
- Race conditions on shared resources
- Basic error handling (`ConnectionRefusedError`, `ConnectionResetError`, `KeyboardInterrupt`)

---

## Configuration

Host and port are set at the top of both files. Change them if port `5000` is already in use:

```python
HOST = "127.0.0.1"
PORT = 5000
```

---

## Autho

**Your Name**
Course: Computer Networks – Lab 3
