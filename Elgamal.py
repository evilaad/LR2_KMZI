import random
import sys

def generate_prime(bits):
    """Генерация случайного простого числа заданной битовой длины."""
    while True:
        candidate = random.getrandbits(bits)
        candidate |= 1  # Убедимся, что число нечётное
        if is_prime(candidate):
            return candidate

def is_prime(n, rounds=5):
    """Тест Миллера-Рабина для проверки простоты числа."""
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Преобразование числа в вид (2^s) * d
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def miller_rabin_trial(a):
        """Один раунд проверки на основе базового числа a."""
        x = pow(a, d, n)
        if x in (1, n - 1):
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for _ in range(rounds):
        a = random.randint(2, n - 2)
        if not miller_rabin_trial(a):
            return False
    return True

def is_generator(g, p):
    """Проверка, является ли g генератором в группе чисел по модулю p."""
    if g <= 1 or g >= p:
        return False
    factors = prime_factors(p - 1)
    for factor in factors:
        if pow(g, (p - 1) // factor, p) == 1:
            return False
    return True

def prime_factors(n):
    """Разложение числа на простые множители."""
    factors = set()
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.add(divisor)
            n //= divisor
        divisor += 1
    if n > 1:
        factors.add(n)
    return factors

def generate_keys(p):
    """Генерация пары ключей (приватный, публичный) и генератора g."""
    while True:
        g = random.randint(2, p - 2)
        if is_generator(g, p):
            break
    private_key = random.randint(2, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key, g

def encrypt(message, public_key, g, p):
    """Шифрование сообщения с использованием публичного ключа."""
    k = random.randint(2, p - 2)  # Временный ключ
    c1 = pow(g, k, p)
    c2 = (message * pow(public_key, k, p)) % p
    return c1, c2

def decrypt(c1, c2, private_key, p):
    """Дешифрование сообщения с использованием приватного ключа."""
    s = pow(c1, private_key, p)  # s = c1^private_key mod p
    message = (c2 * pow(s, p - 2, p)) % p  # Используем обратный элемент
    return message

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
    alice_private_key, alice_public_key, generator = generate_keys(prime)
    print(f"Алиса - закрытый ключ: {alice_private_key}, открытый ключ: {alice_public_key}, генератор: {generator}")

    # Генерация ключей для Боба
    bob_private_key, bob_public_key, _ = generate_keys(prime)
    print(f"Боб - закрытый ключ: {bob_private_key}, открытый ключ: {bob_public_key}")

    # Боб шифрует сообщение и отправляет его Алисе
    original_message = 24
    print(f"Исходное сообщение Боба: {original_message}")
    c1, c2 = encrypt(original_message, alice_public_key, generator, prime)
    print(f"Зашифрованное сообщение Боба (c1, c2): ({c1}, {c2})")

    # Алиса расшифровывает сообщение от Боба
    decrypted_message = decrypt(c1, c2, alice_private_key, prime)
    print(f"Расшифрованное сообщение Алисы: {decrypted_message}")

if __name__ == "__main__":
    main()
