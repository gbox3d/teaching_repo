"""Independent UDP discovery transport."""

import errno
import socket
import threading


class UdpServer:
    def __init__(self, protocol, host, port, *, log=lambda message: None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.log = log
        self._socket = None
        self._thread = None
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._running = False
        self._error = None

    def bind(self):
        if self._socket is not None or self._stop.is_set():
            raise RuntimeError("UDP server has already been bound or closed")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            sock.bind((self.host, self.port))
            sock.settimeout(0.2)
        except Exception as exc:
            sock.close()
            with self._lock:
                self._error = str(exc)
            raise
        self._socket = sock
        self.port = sock.getsockname()[1]

    def start(self):
        if self._socket is None or self._stop.is_set():
            raise RuntimeError("UDP server must be bound before start")
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, name="wleno-udp", daemon=True)
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
            return {"running": self._running, "port": self.port, "error": self._error}

    def close(self):
        self._stop.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(2.5)
        elif thread is None and self._socket is not None:
            self._socket.close()
            self._socket = None

    def _run(self):
        try:
            while not self._stop.is_set():
                try:
                    data, address = self._socket.recvfrom(65535)
                except socket.timeout:
                    continue
                except OSError as exc:
                    # ICMP errors on Windows and oversized datagrams must not
                    # turn one failed discovery reply into a stopped service.
                    if exc.errno in (errno.EBADF, errno.ENOTSOCK):
                        raise
                    continue
                reply = self.protocol.handle_udp(data)
                if reply is not None:
                    try:
                        self._socket.sendto(reply, address)
                    except OSError:
                        continue
        except Exception as exc:
            with self._lock:
                self._error = f"{type(exc).__name__}: {exc}"
            try:
                self.log(f"UDP: {self._error}")
            except Exception:
                pass
        finally:
            if self._socket is not None:
                self._socket.close()
                self._socket = None
            with self._lock:
                self._running = False
