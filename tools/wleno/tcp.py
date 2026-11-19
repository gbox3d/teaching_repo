"""Bounded, line-oriented TCP transport; the protocol owns all message rules."""

from dataclasses import dataclass, field
import queue
import selectors
import socket
import threading


MAX_LINE = 64 * 1024
MAX_OUTPUT = 256 * 1024
# Leave room below Windows SelectSelector's socket limit.
MAX_CLIENTS = 128


@dataclass(eq=False)
class _Client:
    sock: socket.socket
    cursor: int
    incoming: bytearray = field(default_factory=bytearray)
    outgoing: bytearray = field(default_factory=bytearray)


class TcpServer:
    def __init__(self, protocol, host, port, *, log=lambda message: None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.log = log
        self._socket = None
        self._thread = None
        self._selector = None
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._clients = set()
        self._drops = queue.SimpleQueue()
        self._running = False
        self._error = None

    def bind(self):
        if self._socket is not None or self._stop.is_set():
            raise RuntimeError("TCP server has already been bound or closed")
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            else:
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.host, self.port))
            listener.listen(32)
            listener.setblocking(False)
        except Exception as exc:
            listener.close()
            with self._lock:
                self._error = str(exc)
            raise
        self._socket = listener
        self.port = listener.getsockname()[1]

    def start(self):
        if self._socket is None or self._stop.is_set():
            raise RuntimeError("TCP server must be bound before start")
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, name="wleno-tcp", daemon=True)
        with self._lock:
            self._running = True
        try:
            self._thread.start()
        except Exception:
            with self._lock:
                self._running = False
            self._thread = None
            raise

    def status(self):
        with self._lock:
            return {"running": self._running, "port": self.port,
                    "error": self._error, "clients": len(self._clients)}

    def drop_all(self):
        # Only the owner thread closes clients. New arrivals are not selected.
        with self._lock:
            selected = tuple(self._clients)
        if selected:
            self._drops.put(selected)
        return len(selected)

    def close(self):
        self._stop.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(2.5)
        elif thread is None and self._socket is not None:
            self._socket.close()
            self._socket = None

    def _remove(self, client):
        with self._lock:
            if client not in self._clients:
                return
            self._clients.remove(client)
        try:
            self._selector.unregister(client.sock)
        except (KeyError, ValueError):
            pass
        client.sock.close()

    def _enqueue(self, client, data):
        if len(client.outgoing) + len(data) > MAX_OUTPUT:
            self._remove(client)
            return False
        client.outgoing.extend(data)
        self._selector.modify(client.sock, selectors.EVENT_READ | selectors.EVENT_WRITE, client)
        return True

    def _events(self, client):
        cursor, lines, missed = self.protocol.events_after(client.cursor)
        if missed:
            self._remove(client)
            return False
        for line in lines:
            if not self._enqueue(client, line):
                return False
        client.cursor = cursor
        return True

    def _accept(self):
        # A fixed batch prevents incoming connections from starving existing ones.
        for _ in range(32):
            try:
                conn, _ = self._socket.accept()
            except BlockingIOError:
                return
            except ConnectionError:
                continue
            if len(self._clients) >= MAX_CLIENTS:
                conn.close()
                continue
            try:
                conn.setblocking(False)
                client = _Client(conn, self.protocol.event_cursor())
                self._selector.register(conn, selectors.EVENT_READ, client)
            except Exception:
                conn.close()
                raise
            with self._lock:
                self._clients.add(client)
            self._enqueue(client, self.protocol.hello())

    def _read(self, client):
        try:
            data = client.sock.recv(16384)
        except BlockingIOError:
            return
        except OSError:
            self._remove(client)
            return
        if not data:
            self._remove(client)
            return
        client.incoming.extend(data)
        while True:
            newline = client.incoming.find(b"\n")
            if newline < 0:
                if len(client.incoming) >= MAX_LINE:
                    self._remove(client)
                return
            if newline + 1 > MAX_LINE:
                self._remove(client)
                return
            line = bytes(client.incoming[:newline + 1])
            del client.incoming[:newline + 1]
            if not self._events(client):
                return
            reply = self.protocol.handle_tcp(line)
            if reply is not None and not self._enqueue(client, reply):
                return

    def _write(self, client):
        try:
            sent = client.sock.send(client.outgoing)
        except BlockingIOError:
            return
        except OSError:
            self._remove(client)
            return
        if sent == 0:
            self._remove(client)
            return
        del client.outgoing[:sent]
        if not client.outgoing:
            self._selector.modify(client.sock, selectors.EVENT_READ, client)

    def _run(self):
        try:
            with selectors.DefaultSelector() as selector:
                self._selector = selector
                selector.register(self._socket, selectors.EVENT_READ)
                while not self._stop.is_set():
                    while not self._drops.empty():
                        for client in self._drops.get_nowait():
                            self._remove(client)
                    for client in tuple(self._clients):
                        self._events(client)
                    for key, mask in selector.select(0.05):
                        client = key.data
                        if client is None:
                            self._accept()
                            continue
                        if client not in self._clients:
                            continue
                        if mask & selectors.EVENT_READ:
                            self._read(client)
                        if client in self._clients and mask & selectors.EVENT_WRITE:
                            self._write(client)
        except Exception as exc:
            with self._lock:
                self._error = f"{type(exc).__name__}: {exc}"
            try:
                self.log(f"TCP: {self._error}")
            except Exception:
                pass
        finally:
            # The selector context has closed; socket closure remains our duty.
            for client in tuple(self._clients):
                client.sock.close()
            with self._lock:
                self._clients.clear()
                self._running = False
            if self._socket is not None:
                self._socket.close()
                self._socket = None
