import socket
import threading
import rsa
import struct
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
        self.r = rsa.RSA()
        encrypt, decrypt, n = self.r.gen_key_pair()
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
            print(f'Exchanging info with {username}...')
            # print('Sending server modulo...')
            c.sendall(n.to_bytes(256))
            # print('Sending server public key...')
            c.sendall(self.public_key.to_bytes(128))

            threading.Thread(target=self.handle_client,args=(c,)).start()

            print(f"{username} connected.")


    def broadcast(self, msg: str, sender_socket=None, hash_message=None):
        """Sends an encrypted message and its hash to all clients except the sender."""
        for client in self.clients:
            if client == sender_socket:
                continue
        
            try:
                client_public_key = self.client_info_lookup[client]['client_pub']
                client_modulo = self.client_info_lookup[client]['mod']

                encrypted_msg = self.r.encode_message(msg, client_public_key, client_modulo)
                message_header = struct.pack(">I", len(encrypted_msg))
                if not hash_message:
                    hash_message = ''.encode('utf-8')
                hash_header = struct.pack(">I", len(hash_message))

                full_massage = message_header +  encrypted_msg  + hash_header + hash_message
                client.send(full_massage)
            except Exception as e:
                print(f"[server]: Failed to send message to {self.client_info_lookup[client]['username']}: {e}")

    def handle_client(self, c: socket):
        """Handles incoming messages from a single client."""
        while True:
            message_header = c.recv(4)
            len_message = struct.unpack(">I",  message_header)[0]
            message = c.recv(len_message)
            message = self.r.decode_message(message, self.private_key, self.modulo)
            message_hash = c.recv(4)
            hash_len = struct.unpack(">I", message_hash)[0]
            hashed_message = c.recv(hash_len)
            self.broadcast(message, c, hashed_message)

if __name__ == "__main__":
    s = Server(9001)
    s.start()