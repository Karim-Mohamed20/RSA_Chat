from my_functions import *


text = "Welcome to Egypt"
groups = separate_groups(text)
numbers = encode(groups)
prime_1 = generate_random_prime(16)
prime_2 = generate_random_prime(16)
n = prime_1*prime_2
print(prime_1, prime_2, n)
num_of_bits = 32
public_key, private_key = generate_keys_with_specific_num_of_bits(
    prime_1, prime_2, num_of_bits)
print("public_key:", public_key)
time_before_encryption = datetime.datetime.now()
Cipher = encryption(numbers, public_key, n)
time_after_encryption = datetime.datetime.now()
print("cipher", Cipher)
messageNumbers = decryption(Cipher, private_key, n)
message = ''.join(decode(messageNumbers)).strip()
print("message", message)
print("time_for_encryption", time_after_encryption-time_before_encryption)
