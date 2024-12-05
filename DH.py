import random
import sys

def find_prime(bit_length):
    """Генерация простого числа с заданной длиной в битах."""
    candidate = random.getrandbits(bit_length)
    candidate |= 1  # Делаем число нечётным
    while not test_prime(candidate):
        candidate += 2
    return candidate

def test_prime(num, iterations=5):
    """Проверка числа на простоту с помощью теста Миллера-Рабина."""
    if num < 2:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0:
        return False

    # Представление числа в виде (2^s) * d
    d, s = num - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Вспомогательная функция для проверки условия теста
    def miller_rabin_trial(base):
        x = pow(base, d, num)
        if x in (1, num - 1):
            return True
        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                return True
        return False

    # Проведение нескольких раундов теста
    for _ in range(iterations):
        test_base = random.randint(2, num - 2)
        if not miller_rabin_trial(test_base):
            return False
    return True

def generate_keypair(prime, generator):
    """Создание пары ключей: приватного и публичного."""
    private = random.randint(2, prime - 2)
    public = pow(generator, private, prime)
    return private, public

def compute_session_key(private, public, prime):
    """Генерация общего сеансового ключа."""
    return pow(public, private, prime)

def xor_crypt(data, key):
    """Шифрование или дешифрование текста с помощью XOR."""
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, byteorder='big')
    return bytes(char ^ key_bytes[i % len(key_bytes)] for i, char in enumerate(data))

def main():
    # Пользовательский ввод
    bit_length = int(input("Введите длину ключа в битах (кратно 8): "))
    if bit_length % 8 != 0:
        print("Ошибка: длина ключа должна быть кратна 8.")
        sys.exit(1)

    # Генерация простого числа и генератора
    prime = find_prime(bit_length)
    generator = random.randint(2, prime - 2)
    print(f"Простое число (p): {prime}")
    print(f"Генератор (g): {generator}")

    # Создание ключей для Алисы и Боба
    alice_private, alice_public = generate_keypair(prime, generator)
    bob_private, bob_public = generate_keypair(prime, generator)

    print(f"Алиса - закрытый ключ: {alice_private}, открытый ключ: {alice_public}")
    print(f"Боб - закрытый ключ: {bob_private}, открытый ключ: {bob_public}")

    # Обмен и вычисление сеансовых ключей
    alice_session_key = compute_session_key(alice_private, bob_public, prime)
    bob_session_key = compute_session_key(bob_private, alice_public, prime)

    print(f"Сеансовый ключ Алисы: {alice_session_key}")
    print(f"Сеансовый ключ Боба: {bob_session_key}")

    if alice_session_key != bob_session_key:
        print("Ошибка: сеансовые ключи не совпадают!")
        sys.exit(1)
    print("Сеансовые ключи совпадают.")

    # Тест шифрования и дешифрования
    message = "Привет, это секретное сообщение!".encode()
    print(f"Исходное сообщение: {message.decode()}")

    encrypted = xor_crypt(message, alice_session_key)
    print(f"Зашифрованное сообщение: {encrypted.hex()}")

    decrypted = xor_crypt(encrypted, alice_session_key)
    print(f"Расшифрованное сообщение: {decrypted.decode()}")

if __name__ == "__main__":
    main()
