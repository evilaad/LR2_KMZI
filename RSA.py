import random
import sys


def generate_prime(bits):
    """Генерирует простое число заданного размера."""
    while True:
        candidate = random.getrandbits(bits) | 1  # Убедимся, что число нечетное
        if is_prime(candidate):
            return candidate


def is_prime(n, iterations=5):
    """Проверяет, является ли число простым с использованием теста Миллера-Рабина."""
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def miller_test(a):
        x = pow(a, d, n)
        if x in (1, n - 1):
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for _ in range(iterations):
        test_value = random.randint(2, n - 2)
        if not miller_test(test_value):
            return False
    return True


def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def mod_inverse(a, m):
    """Вычисляет обратный элемент по модулю."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} не имеет обратного элемента по модулю {m}")
    return x % m


def generate_keys(key_size):
    """Генерирует пару ключей (публичный и приватный)."""
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(3, phi - 1)
        if extended_gcd(e, phi)[0] == 1:
            break

    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(message, public_key):
    """Шифрует сообщение с использованием публичного ключа."""
    e, n = public_key
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    """Расшифровывает сообщение с использованием приватного ключа."""
    d, n = private_key
    return pow(ciphertext, d, n)


def main():
    sys.setrecursionlimit(2000)  # Увеличиваем глубину рекурсии для больших ключей
    key_size = int(input("Введите размерность ключа (бит, кратно 8): "))
    if key_size % 8 != 0:
        print("Размер ключа должен быть кратен 8.")
        sys.exit(1)

    print("\n=== Генерация ключей для Алисы ===")
    alice_public_key, alice_private_key = generate_keys(key_size)
    print(f"Публичный ключ Алисы: {alice_public_key}")
    print(f"Приватный ключ Алисы: {alice_private_key}")

    print("\n=== Генерация ключей для Боба ===")
    bob_public_key, bob_private_key = generate_keys(key_size)
    print(f"Публичный ключ Боба: {bob_public_key}")
    print(f"Приватный ключ Боба: {bob_private_key}")

    # Алиса шифрует и отправляет сообщение Бобу
    original_message = 42
    print(f"\nИсходное сообщение Алисы: {original_message}")
    encrypted_message = encrypt(original_message, bob_public_key)
    print(f"Зашифрованное сообщение Алисы: {encrypted_message}")

    decrypted_message = decrypt(encrypted_message, bob_private_key)
    print(f"Расшифрованное сообщение Боба: {decrypted_message}")

    # Боб шифрует и отправляет ответ Алисе
    response_message = 24
    print(f"\nОтветное сообщение Боба: {response_message}")
    encrypted_response = encrypt(response_message, alice_public_key)
    print(f"Зашифрованный ответ Боба: {encrypted_response}")

    decrypted_response = decrypt(encrypted_response, alice_private_key)
    print(f"Расшифрованный ответ Алисы: {decrypted_response}")


if __name__ == "__main__":
    main()
