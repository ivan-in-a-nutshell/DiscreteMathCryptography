from math import gcd
from random import randint, SystemRandom
from time import perf_counter

class RSA:
    def gen_key_pair(self):
        """Generate public and private key pair"""
        p = self.__get_prime()
        q = self.__get_prime()
        n = p * q
        # print(n)
        phi = (p - 1) * (q - 1)
        encrypt = self.__generate_key(phi)
        decrypt = self.__get_inverse(encrypt, phi)

        return encrypt, decrypt, n

    def __get_prime(self):
        """Generate a BIG prime number."""
        number = randint(int(1e199), int(1e200))
        while not self.__is_prime(number):
            number += 1

        return number

    @staticmethod
    def __is_prime(n, k=100):
        if n < 2 or (n != 2 and not n & 1):
            return False
        if n < 6:
            return True
        random_gen = SystemRandom()
        for _ in range(k):
            a = random_gen.randrange(2, n - 1)
            exp = n - 1
            while not exp & 1:
                exp >>= 1
            if pow(a, exp, n) == 1:
                continue
            while exp < n - 1:
                if pow(a, exp, n) == n - 1:
                    break
                exp <<= 1
            else:
                return False
        return True

    @staticmethod
    def __generate_key(phi):
        """Generating a public encryption key"""
        # Most common value
        e = 65537
        if e >= phi:
            raise RuntimeError('Encryption key bigger than phi')
        i = 0
        while gcd(phi, e) != 1:
            e += 2 ** i
        return e

    @staticmethod
    def __get_inverse(e, phi):
        """Calculate the inverse of a public encryption key which results in a private decryption key"""

        t, new_t = 0, 1
        r, new_r = phi, e

        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r

        if r > 1:
            raise RuntimeError('Number is not invertible')
        if t < 0:
            t += phi

        return t
