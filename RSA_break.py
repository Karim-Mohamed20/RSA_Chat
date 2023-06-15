from my_functions import *


def break_RSA(n, e):
    factors = factorize(n)
    for i in range(len(factors)):
        p = factors[i]
        q = n // p
        if p * q == n:
            print("Found factors p and q:", p, q)
            phi = (p-1)*(q-1)
            d = multiplicative_inverse_2(e, phi)
            return int(d)
    print("Failed to factorize n")
    return None


n = 2566394203
e = 1644264949
C = [1556655120, 369579855, 1106780884, 1590907798]

time_before_break = datetime.datetime.now()
d = break_RSA(n, e)
time_after_break = datetime.datetime.now()
print("time_for_break", time_after_break-time_before_break)
message = ''.join(decode(decryption(C, d, n))).strip()

if d is not None:
    print("Private key d found:", d)
    print("Original message:", message)
