import socket

class server:

    def __init__(self, ip_addr='0.0.0.0', port=9091):
        self.server = socket.socket()
        self.ip_addr = ip_addr
        self.port = port
        self.server.bind((self.ip_addr, self.port))
        self.server.listen(2)

    def recv_commands(self):
        try:
            conn, _ = self.server.accept()
            data = conn.recv(2056).decode()
            print(f"server recieved command: {data}")
            if data.lower().find('measure') != -1:
                print('yea')
                conn.send('1 2 3'.encode())
            conn.close()
        except:
            print('Problems...')
        

if __name__ == '__main__':
    s = server()
    while True:
        s.recv_commands()