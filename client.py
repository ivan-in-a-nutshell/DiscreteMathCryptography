import socket
import threading
import rsa

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return
        print('Sending username...')
        self.s.send(self.username.encode())

        # create key pairs
        r = rsa.RSA()
        encrypt, decrypt, n = r.gen_key_pair()
        self.modulo = n
        self.public_key = encrypt
        self.private_key = decrypt

        print(f'Sending modulo...')
        self.s.sendall(n.to_bytes(256))
        print('Sending public key...')
        self.s.sendall(self.public_key.to_bytes(128))
        print('Receiving server mod key...')
        self.other_mod_key = int.from_bytes(self.s.recv(256))
        print('Receiving server public key...')
        self.other_pub_key = int.from_bytes(self.s.recv(128))
        print('Client started...')
        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()

            # decrypt message

            # ... 


            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message

            # ...

            self.s.send(message.encode())



if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()