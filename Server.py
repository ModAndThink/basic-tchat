import socket
import threading

class Server(object):
    def __init__(self,port=5050,ip="0.0.0.0"):
        self.PORT = port
        self.HEADER = 64
        self.SERVER = ip
        self.ADDR = (self.SERVER,self.PORT)
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.clients = []

        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.start()

    def send(self,msg,conn):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(self.FORMAT)
        print(msg)

        self.send("30939211271",conn)

        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(self.FORMAT)
        
        listPos = len(self.clients)
        self.clients.append((conn,msg))
        connected = True
        
        while connected:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(self.FORMAT)
                    print(msg)
                    if msg == self.DISCONNECT_MESSAGE:
                        connected = False
                    elif msg == "TOTAL_CLIENT":
                        self.send("Server|"+str(len(self.clients)),conn)
                    else:
                        for clientPos in range(0,len(self.clients)):
                            if clientPos != listPos:
                                self.send(msg,self.clients[clientPos][0])
            except:
                connected=False
                for clientPos in range(0,len(self.clients)):
                    if clientPos != listPos:
                        self.send("The assistant|"+self.clients[listPos][1]+" leave lobby",self.clients[clientPos][0])
                
        conn.close()
        self.clients.remove(self.clients[listPos])

    def loop(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client,args = (conn,addr))
            thread.start()
        
    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening on {self.SERVER}")
        thread = threading.Thread(target=self.loop)
        thread.start()

if __name__ == "__main__":
    Server()
