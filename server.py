import socket
import threading
import rsa

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.client_info_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # generate keys ...
        r = rsa.RSA()
        encrypt, decrypt, n = r.gen_key_pair()
        self.modulo = n
        self.public_key = encrypt
        self.private_key = decrypt
        print("Server started...")
        while True:
            print('Waiting for connection...')
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            n_mod = int.from_bytes(c.recv(256))
            client_pub = int.from_bytes(c.recv(128))
            print(f'{username} connected')
            self.broadcast(f'new person has joined: {username}')
            self.client_info_lookup[c] = {'username': username, 'mod': n_mod, 'client_pub': client_pub}
            self.clients.append(c)

            # send public key to the client
            print('Sending server modulo...')
            c.sendall(n.to_bytes(256))
            print('Sending server public key...')
            c.sendall(self.public_key.to_bytes(128))

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:

            # encrypt the message

            # ...

            client.send(msg.encode())
            client.send(self.client_info_lookup[client]['client_pub'].to_bytes(128))

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()