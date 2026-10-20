# Socket Programming

UDP and TCP socket programming practice from my network course. Python 3, Ubuntu.

## Progress

- [x] UDP server
- [x] UDP client
- [x] TCP server
- [x] TCP client

## What I coded

**`udp_server.py`**: A UDP server on port 12000. It receives a message, converts it to UPPERCASE, and sends it back to the sender.

Steps: create socket → `bind` to port → `recvfrom` (get data + sender address) → `decode` → `upper` → `encode` → `sendto` sender address.

**`udp_client.py`**: Sends a sentence to the server and prints the UPPERCASE reply. If the server does not answer in 5 seconds, it prints "Server is not responding".

Steps: create socket → `settimeout(5)` → `input` → `encode` → `sendto` server address → `recvfrom` (inside `try`) → `decode` → print → `close`.

**`tcp_server.py`**: The same UPPERCASE server, with TCP on port 4980. It serves one client at a time.

Steps: create socket → `bind` → `listen` → loop: `accept` (new socket) → `recv` → `upper` → `send` → `close` the new socket.

**`tcp_client.py`**: Connects to the TCP server, sends a sentence, prints the reply.

Steps: create socket → `connect` → `input` → `send` → `recv` → print → `close`.

## Key ideas

- **Socket**: The program's door to the network. The OS sends the packets, not my program.
- **UDP**: Connectionless, like a letter. Every message carries its own address. No delivery guarantee.
- **TCP**: Connection-oriented, like a phone call. Connect first, then talk. It is a byte stream (no message boundaries).
- **Ephemeral port**: The client does not need `bind`. The OS gives it a random free port. The server learns this port from the incoming packet.
- **Demultiplexing**: How the OS decides which socket gets an incoming packet.
  - UDP socket = (dest IP, dest port)
  - TCP socket = (src IP, src port, dest IP, dest port), the 4-tuple. That is why `accept()` returns a new socket for every client.
- **Listening socket vs connection socket**: The listening socket is a switchboard. It never sends or receives data. It only gives new sockets. I close the connection socket after each client, never the listening one.
- **Why `recv` has no address in TCP**: After `accept` / `connect`, the peer address is fixed inside the socket. Every byte on this socket comes from the same peer.

## UDP experiments

**1. Same UDP server twice on the same port?**
The second one fails: `OSError: [Errno 98] Address already in use`. A UDP socket is identified only by (IP, port). If two sockets had the same pair, the OS could not know which one should get the packet.

**2. Where does the client port come from?**
`getsockname()` before `sendto`: `('0.0.0.0', 0)`. After: `('0.0.0.0', 42187)`. The OS assigns the port at the first `sendto` (implicit bind). The server saw the same port. It changes every run.

**3. What if the server is down?**
`sendto` does not fail. UDP has no connection, so the client cannot know the server is gone. `recvfrom` waits forever. Fix: `settimeout()` and catch `TimeoutError` with `try / except`.

## TCP experiments

**1. Two sockets on the same port (`ss -tanp`)**
While one `nc` was connected, port 4980 had:
- `LISTEN 127.0.0.1:4980 → *` (python, fd=3): the listening socket
- `ESTAB 127.0.0.1:4980 → 127.0.0.1:46056` (python, fd=4): the socket from `accept`
- `ESTAB 127.0.0.1:46056 → 127.0.0.1:4980` (nc): the other end of the same connection (mirror)

Two sockets share port 4980. TCP allows this because the 4-tuples are different.

**2. Who does the 3-way handshake?**
The server was busy with client 1. A second `nc` connected. It was still `ESTAB`, with **no process** on the server side, and `LISTEN` showed `Recv-Q = 1`.
- The **OS kernel** does the handshake, not `accept()`.
- Ready connections wait in the **accept queue (backlog)**. `accept()` only takes one from the queue.
- `listen()` default backlog = 128 (`Send-Q` of the LISTEN line).
- Data a program has not read waits in the OS **receive buffer**. `recv()` reads from this buffer.

**3. Closing a connection**
After the server called `close()` but `nc` was still open:
- Server side: `FIN-WAIT-2` (no process): "I sent FIN, waiting for your FIN." The OS owns the socket now.
- `nc` side: `CLOSE-WAIT`: "The peer closed. My program must close too."
- Each side closes its own direction. `FIN-WAIT-2` times out after about 60 seconds.

**4. Where does the TCP client port come from?**
`getsockname()` before `connect`: `('0.0.0.0', 0)`. After: `('127.0.0.1', 42492)`.
- The port is assigned at `connect`, because the first handshake packet (SYN) needs a source port.
- The IP is also fixed (not `0.0.0.0`), because a connection is a fixed 4-tuple.

**5. What if the server is down?**
`connect` fails **immediately**: `ConnectionRefusedError: [Errno 111] Connection refused`. The server's OS has no LISTEN socket on the port, so it answers the SYN with **RST** (reset). UDP waited for a timeout; TCP knows at once.

## Notes to remember

- `bind` and `connect` take **one tuple**: `bind(("", 12000))`, not `bind("", 12000)`
- Sockets send `bytes`, not `str`: use `encode()` / `decode()`
- `recvfrom` returns a pair: `(data, (ip, port))`. `accept` returns a pair: `(new_socket, (ip, port))`
- Ports below 1024 need root. Use a high port.
- Python docs: `socket` is in the Library Reference, not the Tutorial. Offline: `help(socket.socket.recvfrom)`
- Read a doc entry with 3 questions: What does it take? What does it return? Anything to be careful about?
- Make an error on purpose to learn its name, then catch it with `except`.

## Test

```bash
# UDP
python3 udp_server.py      # terminal 1
nc -u 127.0.0.1 12000          # terminal 2 (or: python3 udp_client.py)
ss -uanp | grep 12000          # terminal 3

# TCP
python3 tcp_server.py      # terminal 1
nc 127.0.0.1 4980              # terminal 2 (or: python3 tcp_client.py)
ss -tanp | grep 4980           # terminal 3
```

`ss` flags: **u**dp / **t**cp, **a**ll (show UNCONN and LISTEN too), **n**umeric ports, **p**rocess name.