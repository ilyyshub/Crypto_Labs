"""Laboratory 3, task 3.2: Vigenere with the 31-letter Romanian alphabet."""

import unicodedata

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
ALLOWED = ALPHABET + ALPHABET.lower()


def normalize(text, allow_spaces=False):
    """Validate letters, optionally remove spaces, and return uppercase text."""
    text = unicodedata.normalize("NFC", text)

    if allow_spaces:
        text = text.replace(" ", "")

    if not text:
        raise ValueError("Textul trebuie să conțină cel puțin o literă.")

    # Check before uppercasing: characters such as 'ß' must not become 'SS'.
    for letter in text:
        if letter not in ALLOWED:
            raise ValueError(
                "Caractere permise: " + ALPHABET
                + " și variantele lor minuscule. "
                + "Doar spațiile simple din mesaj sunt eliminate."
            )

    return text.upper()


def validate_key(key):
    """A key contains at least seven Romanian letters and no spaces."""
    key = normalize(key)
    if len(key) < 7:
        raise ValueError("Cheia trebuie să conțină cel puțin 7 litere.")
    return key


def vigenere(text, key, decrypt=False):
    """Encrypt or decrypt; spaces are removed and the key repeats."""
    text = normalize(text, allow_spaces=True)
    key = validate_key(key)
    result = ""
    direction = -1 if decrypt else 1

    for i, letter in enumerate(text):
        message_value = ALPHABET.index(letter)
        key_letter = key[i % len(key)]
        key_value = ALPHABET.index(key_letter)
        value = (message_value + direction * key_value) % len(ALPHABET)
        result += ALPHABET[value]

    return result


def main():
    while True:
        print("\n1. Criptare\n2. Decriptare\n0. Ieșire")
        operation = input("Alegeți operația: ")

        if operation == "0":
            break
        if operation not in ("1", "2"):
            print("Eroare: alegeți 1, 2 sau 0.")
            continue

        try:
            key = validate_key(input("Cheia (minimum 7 litere): "))
            prompt = "Criptograma: " if operation == "2" else "Mesajul: "
            text = input(prompt)
            result = vigenere(text, key, decrypt=(operation == "2"))
            print("Rezultat:", result)
        except ValueError as error:
            print("Eroare:", error)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram încheiat.")
