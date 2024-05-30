import socket
import threading
import io
import select
import COMMON.Telegram as Tel
import COMMON.Common as Cmn

def communicate(server, callback):
    try:
        tel = Tel.Telegram()
        while Server.run:
            readlist, _, _ = select.select([server], [], [], 0.5)
            for r in readlist:
                message, addr = r.recvfrom(Tel.BUFSIZE)
                buffer = io.BytesIO(message)
                buffer.readinto(tel)
                if tel.value < Cmn.LOW_VALUE or tel.value > Cmn.HIGH_VALUE:
                    break
                value = callback(tel.channel, tel.value)
                if value == None:
                    break
                response = io.BytesIO()
                response.write(Tel.Telegram(tel.channel, value))
                r.sendto(response.getvalue(), addr)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        server.close()

class Server:
    run = False
    def __init__(self):
        self.server = None
        self.thread = None
        Server.run = False
    def start(self, callback):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((Cmn.HOST, Cmn.PORT))
        self.thread = threading.Thread(target=communicate, args=(self.server, callback))
        Server.run = True
        self.thread.start()
    def close(self):
        Server.run = False
