ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DECRYPTED = "BQFUJYNCRGVKZODSHWLAPETIXM"


# Replace each letter using the two alphabet strings.
def substitute(text, source, target):
    result = ""

    for letter in text:
        if letter in source:
            position = source.index(letter)
            result += target[position]
        elif letter in source.lower():
            position = source.index(letter.upper())
            result += target[position].lower()
        else:
            result += letter

    return result


# 1. Read the ciphertext without removing spaces.
with open("variant6_ciphertext.txt", encoding="utf-8") as file:
    ciphertext = file.read()


# 2. Count uppercase and lowercase English letters together.
counts = {}
total = 0

for letter in ALPHABET:
    count = ciphertext.count(letter)
    count += ciphertext.count(letter.lower())
    counts[letter] = count
    total += count

print("Total letters:", total)

if total == 0:
    print("The text must contain English letters.")
else:
    print("Letter / Count / Percent")
    for letter in ALPHABET:
        percent = counts[letter] * 100 / total
        print(letter, counts[letter], round(percent, 2))


# 3. Decrypt using the alphabet recovered in the report.
plaintext = substitute(ciphertext, ALPHABET, DECRYPTED)
print("\nDecrypted text:")
print(plaintext)

with open("variant6_plaintext_exact.txt", "w",
          encoding="utf-8") as file:
    file.write(plaintext)


# 4. Reverse the substitution and compare with the input.
restored = substitute(plaintext, DECRYPTED, ALPHABET)
print("\nExact re-encryption:", restored == ciphertext)
