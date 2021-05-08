import select
import socket
import threading
import concurrent.futures
from services import log
from tools.Endlessh import run_endlessh
from tools.Honeyports import run_honeyports
from tools.Invisiport import run_invisiport
from tools.Portspoof import run_portspoof
from tools.Tcprooter import run_tcprooter

SERVER = "192.168.41.129"  # socket.gethostbyname(socket.gethostname())
MAX_WORKERS = 5


class Connection:
    def __init__(self, ports, method):
        self.ports = ports
        self.method = method


class Server:
    def __init__(self, loop):
        self.loop = loop
        self.Conns = {}
        self.Sockets = {}
        self.Servers = []
        self.Ports = []
        return

    def extend(self, name, ports, method=None):
        if name in self.Conns:
            self.Conns[name].ports.extend(ports)
            if method is not None:
                self.Conns[name].method = method
        else:
            self.Conns[name] = Connection(ports, method)
        self.Ports.extend(ports)
        return

    def reduce(self, name, ports=None):
        if ports is not None:
            self.Conns[name].ports = [x for x in self.Conns[name].ports if x not in ports]
            self.Ports = [x for x in self.Ports if x not in ports]
        else:
            del self.Conns[name]
        return

    def initialization(self):
        self.Servers = []
        for port in self.Ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind((SERVER, port))
            log.sintetic_write(log.INFO, "SERVER", "Serving port {} on socket {}".format(port, s.fileno()))

            s.listen()
            self.Servers.append(s)
        return

    def run(self):
        self.loop.run_until_complete(self.init())

    async def init(self):
        self.initialization()

        while True:
            conn, addr = select.select(self.Servers, [], [])[0][0].accept()
            self.Sockets[addr[1]] = conn.dup()
            threading.Thread(target=self.handle_input, args=(conn, addr)).start()

    def handle_input(self, conn, addr):
        log.sintetic_write(log.INFO, "SERVER", "New Connection from {}".format(addr))

        connected = True
        my_ip = conn.getsockname()[0]
        in_port = conn.getsockname()[1]
        mal_ip = addr[0]
        out_port = addr[1]
        ws = self.Sockets[out_port]

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while connected:
                msg = conn.recv(1024).decode(encoding="utf-8", errors="replace")
                if msg:
                    log.sintetic_write(log.WARNING, "SERVER", "Receive something..{} from {}:{} and we reply with {}:{}"
                                       .format(msg, mal_ip, out_port, my_ip, in_port))

                    for name, tool in self.Conns.items():
                        if name == "Endlessh" and in_port in tool.ports:
                            self.loop.run_in_executor(executor, run_endlessh(ws, in_port, mal_ip, msg, tool.method))
                            break
                        if name == "Invisiport" and in_port in tool.ports:
                            self.loop.run_in_executor(executor, run_invisiport(ws, in_port, mal_ip, msg, tool.method))
                            break
                        if name == "Honeyports" and in_port in tool.ports:
                            self.loop.run_in_executor(executor, run_honeyports(ws, mal_ip, msg))
                            break
                        if name == "Portspoof" and in_port in tool.ports:
                            self.loop.run_in_executor(executor, run_portspoof(ws, in_port, mal_ip, msg))
                            break
                        if name == "Tcprooter":
                            self.loop.run_in_executor(executor, run_tcprooter(ws, mal_ip, msg))
                            break
                else:
                    log.sintetic_write(log.INFO, "SERVER", "Closing connection to {}".format(addr))
                    conn.close()
                    del self.Sockets[out_port]
                    connected = False
        return
