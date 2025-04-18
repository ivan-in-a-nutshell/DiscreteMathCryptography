
# Cryptography. RSA and Message Integrity Check (Lab 2)

## Implementation Description

### RSA Algorithm Implementation (`rsa.py`)

The file `rsa.py` contains the implementation of the RSA algorithm.

The function `gen_key_pair(self)` generates a pair of public and private keys. For this, two large prime numbers `p` and `q` are generated randomly. Then the modulus `n = p * q` and Euler’s function `(p - 1)(q - 1)` are calculated. Next, a public key `e` is chosen so that it is coprime with `(p - 1)(q - 1)`, and the private key `d` is calculated as the modular inverse of `e` modulo `(p - 1)(q - 1)`. The method returns a tuple of three elements: public key, private key, and modulus.  
To implement this function, additional functions were also implemented.

The function `__get_prime(self)` generates a large prime number. First, a random number is chosen from the range between 10^199 and 10^200, then it is checked for primality. If the number is not prime, it is gradually increased until a prime number is found. The primality check is done using the Miller–Rabin method.

The function `__is_prime(n, k=100)` checks whether a number is prime using the Miller–Rabin method. The `k` argument sets the number of iterations, which affects the accuracy of the check. If the number passes all checks, it is considered prime.

The function `__generate_key(phi)` generates a public key `e`. It first tries the value `65537`, which is often used in RSA. If it is not coprime with `(p - 1)(q - 1)`, the key is gradually changed until a suitable value is found that satisfies the condition `gcd(e, (p - 1)(q - 1)) == 1`.

The function `__get_inverse(e, phi)` calculates the modular inverse of `e` modulo `(p - 1)(q - 1)`. The extended Euclidean algorithm is used for this. If an inverse does not exist, an error is raised. As a result, the method returns the value `d`.

The function `encode_messedge(message, public_key, modulo)` encrypts a text message using the public key. First, the message is converted into bytes, then into an integer, after which it is encrypted using the formula `c = m^e mod n`. The encrypted number is again converted into bytes and returned.

The function `decode_messedge(message, private_key, modulo)` decrypts a message that was encrypted using the `encode_messedge` method. The received bytes are converted into an integer, which is then decrypted using the formula `m = c^d mod n`. Then the number is converted back into bytes and decoded into a text message using UTF-8 encoding.

---

### Message Integrity Check

To ensure message integrity in the communication system, checking is implemented using the SHA-256 hash function. Each message is sent in encrypted form with a hash calculated before encryption.

On the client side, after the user inputs the text, it is first hashed using SHA-256. Then the message is encrypted using the recipient's public key. Along with the encrypted message, the client sends its length, the hash length, and the hash itself. All of this is packed into one block and sent to the server.

The server, after receiving the message and the hash from the client, re-encrypts the message using the sender's public key and sends it to other clients in the same format along with the received hash.

On the client side receiving the message, the reverse process occurs. First, the message length is read, then the message itself, followed by the hash length and the hash string. After decrypting the message using the private key, the client recalculates the SHA-256 hash of the received text and compares it with the sent hash. If both values match, confirmation is shown that the message was received without changes.

---

### Client and Server Interaction

The client generates a pair of RSA keys, connects to the server, and sends the name and public key. The server replies with its public key. The client encrypts the message, adds the SHA-256 hash, and sends it to the server. The server decrypts it, re-encrypts it for each client, and sends it to them. Clients check message integrity by comparing the received hash with the one they calculate.

---

### Conclusion

The RSA algorithm implementation ensures encryption and decryption of messages using public and private keys. The implemented message integrity check helps detect any changes in the transmitted message.  
However, the system has a limitation on the message length because the whole text is encoded as one big number — when this number becomes larger than the modulus `n`, encryption stops working.  
This problem can be solved by splitting the message into blocks or using hybrid encryption methods that combine symmetric and asymmetric encryption.

---

## Work Distribution

- **Solomiia Hadiichuk** — encryption and decryption of messages, hash checking.
- **Ivan Zarytskyi** — RSA key generation, helper functions for key exchange, sending public keys for encryption on the server.
