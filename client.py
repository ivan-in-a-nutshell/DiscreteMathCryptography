import socket
import threading
import rsa
import hashlib
import struct

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

        name = input("Please, enter your name: ")
        if name:
            self.username = name
        print('Sending username...')
        self.s.send(self.username.encode())

        # create key pairs
        self.r = rsa.RSA()
        encrypt, decrypt, n = self.r.gen_key_pair()
        self.modulo = n
        self.public_key = encrypt
        self.private_key = decrypt

        print('Exchanging information...')
        # print('Sending modulo...')
        self.s.sendall(n.to_bytes(256))
        # print('Sending public key...')
        self.s.sendall(self.public_key.to_bytes(128))
        # print('Receiving server mod key...')
        self.other_mod_key = int.from_bytes(self.s.recv(256))
        # print('Receiving server public key...')
        self.other_pub_key = int.from_bytes(self.s.recv(128))

        print('Client started...')
        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message_header = self.s.recv(4)
            message_len = struct.unpack(">I",  message_header)[0]
            message = self.s.recv(message_len)
            message = self.r.decode_message(message, self.private_key, self.modulo)
               
            hash_header =  self.s.recv(4)
            hash_len = struct.unpack(">I", hash_header)[0]
            hashed_message = self.s.recv(hash_len)
            hashed_message = self.r.decode_message(hashed_message, self.other_pub_key, self.other_mod_key)

            new_hash = str(hashlib.sha256(message.encode()).digest())
            if hashed_message:
                print('Message integrity is intact' if new_hash == hashed_message else 'Message has been tampered with')
            print(message)

    def write_handler(self):
        while True:
            message = input()

            hashed_message = str(hashlib.sha256(message.encode()).digest())
            hashed_message = self.r.encode_message(hashed_message, self.private_key, self.modulo)
            hash_header = struct.pack(">I", len(hashed_message))

            encoded_message = self.r.encode_message(message, self.other_pub_key, self.other_mod_key)
            message_header = struct.pack(">I", len(encoded_message))

            full_massage = message_header + encoded_message + hash_header + hashed_message
            self.s.send(full_massage)

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
