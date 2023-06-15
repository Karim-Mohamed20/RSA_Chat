import random
import datetime
import math


def separate_groups(text):
    groups = []
    for i in range(0, len(text), 5):
        subString = text[i:i+5]
        if (len(subString) < 5):
            subString += ' '*(5-len(subString))
        groups.append(subString)
    return groups


def encode(groups):
    numbers = []
    sum = 0
    for group in groups:
        for i in range(0, len(group)):
            if (group[i].isdigit()):
                sum += int(group[i])*(pow(37, i))
            elif (group[i].isalpha()):
                sum += (ord(group[i].upper())-55)*(pow(37, i))
            else:
                sum += 36*(pow(37, i))
        numbers.append(sum)
        sum = 0
    return numbers


def encryption(M, e, n):
    C = []
    for m in M:
        C.append(pow(m, e, n))
    return C


def decryption(C, d, n):
    M = []
    for c in C:
        M.append(pow(c, d, n))
    return M


def decode(numbers):
    groups = []
    for num in numbers:
        group = ""
        while num > 0:
            rem = num % 37
            if rem < 10:
                group += str(rem)
            elif rem < 36:
                group += chr(rem + 55)
            else:
                group += " "
            num //= 37
        groups.append(group.lower())
    return groups


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    temp = 1+phi
    while ((temp % e) != 0):
        temp = temp + phi
    return temp / e


def generate_keys(p, q):
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse_2(e, phi)
    return e, int(d)


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y


def multiplicative_inverse_2(a, m):
    gcd, x, y = gcd_extended(a, m)
    if gcd != 1:
        raise ValueError("The inverse does not exist")
    else:
        return x % m


def generate_keys_with_specific_num_of_bits(p, q, num_of_bits):
    phi = (p-1) * (q-1)
    min_value = 2**(num_of_bits-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse_2(e, phi)
    return e, int(d)


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num))+1):
        if num % i == 0:
            return False
    return True


def generate_random_prime(bits):
    min_val = 2**(bits-1)
    max_val = 2**bits - 1
    while True:
        rand_num = random.randint(min_val, max_val)
        if is_prime(rand_num):
            return rand_num


def send_encrypted_message(sock, message, e, n):
    groups = separate_groups(message)
    numbers = encode(groups)
    time_before_encryption = datetime.datetime.now()
    encrypted_numbers = encryption(numbers, e, n)
    time_after_encryption = datetime.datetime.now()
    encrypted_message = ' '.join(map(str, encrypted_numbers))
    sock.sendall(encrypted_message.encode())
    return (time_after_encryption-time_before_encryption)


def receive_decrypted_message(sock, d, n):
    encrypted_message = sock.recv(1024).decode()
    encrypted_numbers = list(map(int, encrypted_message.split()))
    time_before_decryption = datetime.datetime.now()
    decrypted_numbers = decryption(encrypted_numbers, d, n)
    time_after_decryption = datetime.datetime.now()
    decrypted_groups = decode(decrypted_numbers)
    return (''.join(decrypted_groups).strip()), (time_after_decryption-time_before_decryption)


def factorize(n):
    factors = []
    while n > 1:
        for i in range(2, int(n)+1):
            if n % i == 0:
                factors.append(i)
                n /= i
                break
    return factors
