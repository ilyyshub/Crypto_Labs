import unicodedata

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"


# Read a valid message or keyword.
def read_letters(prompt, keyword=False):
    while True:
        text = input(prompt)

        # Handle Romanian letters typed using different keyboards.
        text = unicodedata.normalize("NFC", text)
        text = text.replace("Ş", "Ș").replace("ş", "ș")
        text = text.replace("Ţ", "Ț").replace("ţ", "ț")

        # Spaces are allowed in messages, but not in keywords.
        if not keyword:
            text = text.replace(" ", "")

        # Check each character before converting to uppercase.
        valid = True

        for letter in text:
            if letter not in ALPHABET and letter not in ALPHABET.lower():
                print("Invalid character:", repr(letter))
                if keyword:
                    print("Use Romanian letters only; no spaces.")
                else:
                    print("Use Romanian letters and ordinary spaces only.")
                valid = False
                break

        if not valid:
            continue  # Ask for the text again.

        if text == "":
            print("Enter at least one Romanian letter.")
            continue

        if keyword and len(text) < 7:
            print("The keyword must contain at least 7 letters.")
            continue

        return text.upper()


# 1. Choose the cipher.
mode = input("Cipher (1 = plain, 2 = keyword): ")

while mode not in ("1", "2"):
    mode = input("Please enter 1 or 2: ")


# 2. Choose encryption or decryption.
operation = input("Operation (e = encrypt, d = decrypt): ").lower()

while operation not in ("e", "d"):
    operation = input("Please enter e or d: ").lower()


# 3. Read the numeric key.
while True:
    try:
        key = int(input("Key (1-30): "))
    except ValueError:
        print("The key must be an integer from 1 to 30.")
        continue

    if 1 <= key <= 30:
        break

    print("The key must be an integer from 1 to 30.")


# 4. Select or build the alphabet.
alphabet = ALPHABET

if mode == "2":
    keyword = read_letters("Keyword: ", keyword=True)
    alphabet = ""

    # Add each keyword letter once.
    for letter in keyword:
        if letter not in alphabet:
            alphabet += letter

    # Add the remaining Romanian letters.
    for letter in ALPHABET:
        if letter not in alphabet:
            alphabet += letter

    print("Permuted alphabet:", alphabet)


# 5. Read the message.
message = read_letters("Message: ")
print("Normalized text:", message)


# 6. Encrypt or decrypt one letter at a time.
result = ""

for letter in message:
    position = alphabet.index(letter)

    if operation == "e":
        new_position = (position + key) % 31
    else:
        new_position = (position - key) % 31

    result += alphabet[new_position]

print("Result:", result)