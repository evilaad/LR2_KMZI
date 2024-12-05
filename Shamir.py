import random
import sys

def generate_prime(bit_length):
    """Генерация случайного простого числа заданной битовой длины."""
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= 1  # Убедимся, что число нечётное
        if test_prime(candidate):
            return candidate

def test_prime(num, rounds=5):
    """Тест Миллера-Рабина для проверки простоты числа."""
    if num <= 1:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0:
        return False

    # Преобразование числа в вид (2^s) * d
    d, s = num - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def miller_rabin_trial(base):
        """Проверка числа с использованием заданной базы."""
        x = pow(base, d, num)
        if x in (1, num - 1):
            return True
        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                return True
        return False

    for _ in range(rounds):
        base = random.randint(2, num - 2)
        if not miller_rabin_trial(base):
            return False
    return True

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения обратного элемента."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Вычисление обратного элемента по модулю."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Число {a} не имеет обратного элемента по модулю {m}.")
    return x % m

def generate_key_pair(prime):
    """Генерация пары ключей (приватного и публичного)."""
    while True:
        private = random.randint(2, prime - 2)
        try:
            public = mod_inverse(private, prime - 1)
            return private, public
        except ValueError:
            continue

def encrypt(message, public_key, prime):
    """Шифрование сообщения с использованием публичного ключа."""
    return pow(message, public_key, prime)

def decrypt(ciphertext, private_key, prime):
    """Дешифрование сообщения с использованием приватного ключа."""
    return pow(ciphertext, private_key, prime)

def main():
    # Запрос длины ключа у пользователя
    bit_length = int(input("Введите размерность ключа в битах (кратно 8): "))
    if bit_length % 8 != 0:
        print("Ошибка: длина ключа должна быть кратна 8.")
        sys.exit(1)

    # Генерация простого числа
    prime = generate_prime(bit_length)
    print(f"Сгенерировано простое число p: {prime}")

    # Генерация ключей для Алисы
    alice_private, alice_public = generate_key_pair(prime)
    print(f"Алиса - закрытый ключ: {alice_private}, открытый ключ: {alice_public}")

    # Генерация ключей для Боба
    bob_private, bob_public = generate_key_pair(prime)
    print(f"Боб - закрытый ключ: {bob_private}, открытый ключ: {bob_public}")

    # Алиса шифрует сообщение и отправляет его Бобу
    message_from_alice = 42
    print(f"Сообщение от Алисы: {message_from_alice}")
    encrypted_message = encrypt(message_from_alice, bob_public, prime)
    print(f"Зашифрованное сообщение от Алисы: {encrypted_message}")

    # Боб расшифровывает сообщение от Алисы
    decrypted_message = decrypt(encrypted_message, bob_private, prime)
    print(f"Расшифрованное сообщение Бобом: {decrypted_message}")

    # Боб шифрует ответ и отправляет его Алисе
    response_from_bob = 24
    print(f"Ответ от Боба: {response_from_bob}")
    encrypted_response = encrypt(response_from_bob, alice_public, prime)
    print(f"Зашифрованный ответ от Боба: {encrypted_response}")

    # Алиса расшифровывает ответ от Боба
    decrypted_response = decrypt(encrypted_response, alice_private, prime)
    print(f"Расшифрованный ответ Алисы: {decrypted_response}")

if __name__ == "__main__":
    main()
