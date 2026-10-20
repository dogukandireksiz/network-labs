# Socket Programming

UDP and TCP socket programming practice from my network course. Python 3, Ubuntu.

## Progress

- [x] UDP server
- [x] UDP client
- [ ] TCP server
- [ ] TCP client

## What I coded

**`udp/udp_server.py`**: A UDP server on port 12000. It receives a message, converts it to UPPERCASE, and sends it back to the sender.

Steps: create socket → `bind` to port → `recvfrom` (get data + sender address) → `decode` → `upper` → `encode` → `sendto` sender address.

**`udp/udp_client.py`**: Sends a sentence to the server and prints the UPPERCASE reply. If the server does not answer in 5 seconds, it prints "Server is not responding".

Steps: create socket → `settimeout(5)` → `input` → `encode` → `sendto` server address → `recvfrom` (inside `try`) → `decode` → print → `close`.

## Key ideas

- **Socket**: The program's door to the network. The OS sends the packets, not my program.
- **UDP**: Connectionless, like a letter. Every message carries its own address. No delivery guarantee.
- **TCP**: Connection-oriented, like a phone call. Connect first, then talk. It is a byte stream (no message boundaries).
- **Ephemeral port**: The client does not need `bind`. The OS gives it a random free port. The server learns this port from the incoming packet.
- **Demultiplexing**: How the OS decides which socket gets an incoming packet.
  - UDP socket = (dest IP, dest port)
  - TCP socket = (src IP, src port, dest IP, dest port), the 4-tuple. That is why `accept()` returns a new socket for every client.

## Thinking question

**What happens if I run the same UDP server twice on the same port?**

The second one fails: `OSError: [Errno 98] Address already in use`.

A UDP socket is identified only by (IP, port). If two sockets had the same pair, the OS could not know which one should get the packet. So the OS refuses the second `bind`.

## Experiments

**1. Where does the client port come from?**
I printed `getsockname()` before and after `sendto`:
- Before: `('0.0.0.0', 0)` → no port yet
- After: `('0.0.0.0', 42187)` → the OS gave a port

The client port is assigned by the OS at the first `sendto` (implicit bind). The server saw the same port. It changes every run.

**2. What if the server is down?**
`sendto` does not fail. UDP has no connection, so the client cannot know the server is gone. `recvfrom` waits forever. Fix: `settimeout()` and catch `TimeoutError` with `try / except`.

## Notes to remember

- `bind` takes **one tuple**: `bind(("", 12000))`, not `bind("", 12000)`
- Sockets send `bytes`, not `str`: use `encode()` / `decode()`
- `recvfrom` returns a pair: `(data, (ip, port))`
- Ports below 1024 need root. Use a high port.
- Python docs: `socket` is in the Library Reference, not the Tutorial. Offline: `help(socket.socket.recvfrom)`

## Test

```bash
python3 udp/udp_server.py      # terminal 1
ss -ulnp | grep 12000          # terminal 2: is the socket listening?
nc -u 127.0.0.1 12000          # terminal 2: type text, get UPPERCASE back
python3 udp/udp_client.py      # terminal 2: or use my client
```

`ss -uanp`: **u**dp, **a**ll (show UNCONN too), **n**umeric ports, **p**rocess name.