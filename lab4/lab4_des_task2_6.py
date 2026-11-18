"""DES task 2.6: expansion, key mixing, and eight six-bit blocks.
    with known Ki and Ri-1 -> calculate B1B2B3B4B5B6B7B"""

import secrets

E_TABLE = (
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1,
)


def parse_value(text, width, base):
    text = text.replace(" ", "").upper()
    prefix = "0B" if base == 2 else "0X"
    if text.startswith(prefix):
        text = text[2:]
    digits = "01" if base == 2 else "0123456789ABCDEF"
    count = width if base == 2 else width // 4
    if len(text) != count or any(c not in digits for c in text):
        kind = "binary digits (0 or 1)" if base == 2 else "hex digits (0-9, A-F)"
        raise ValueError(f"Enter exactly {count} {kind}.")
    return format(int(text, base), f"0{width}b")


def calculate_blocks(right, key):
    for value, width, name in ((right, 32, "R"), (key, 48, "K")):
        if len(value) != width or any(bit not in "01" for bit in value):
            raise ValueError(f"{name} must contain exactly {width} bits.")
    expanded = "".join(right[position - 1] for position in E_TABLE)
    mixed = "".join(str(int(a) ^ int(b)) for a, b in zip(expanded, key))
    blocks = [mixed[start:start + 6] for start in range(0, 48, 6)]
    return expanded, mixed, blocks


def grouped(bits, size):
    return " ".join(bits[start:start + size] for start in range(0, len(bits), size))


def display_steps(right, key, round_number):
    expanded, mixed, blocks = calculate_blocks(right, key)
    print(f"\nDES ROUND {round_number}: TASK 2.6")
    print(f"R_{round_number - 1} (32 bits): {grouped(right, 4)}")
    print(f"R hex: {int(right, 2):08X}")
    print(f"K_{round_number} (48 bits): {grouped(key, 6)}")
    print(f"K hex: {int(key, 2):012X}")

    print("\n1. E BIT-SELECTION TABLE (input positions, numbered 1-32)")
    for row in range(8):
        print(f"Group {row + 1}: " + " ".join(
            f"{p:2d}" for p in E_TABLE[6 * row:6 * row + 6]))
    print("\n2. XOR TABLE\nE bit | K bit | Result")
    for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
        print(f"  {a}   |   {b}   |   {a ^ b}")

    print("\n3. EVERY EXPANSION SELECTION AND XOR OPERATION")
    print("Output t | R position | R bit = E bit | K bit | XOR | Block")
    for t, source_position in enumerate(E_TABLE):
        print(f"{t + 1:8d} | {source_position:10d} |"
              f"       {expanded[t]}       |   {key[t]}   |"
              f"  {mixed[t]}  | B{t // 6 + 1}")

    print("\n4. EXPANDED R AND KEY MIXING")
    print("E(R): " + grouped(expanded, 6))
    print("K:    " + grouped(key, 6))
    print("XOR:  " + grouped(mixed, 6))
    print(f"E(R) hex: {int(expanded, 2):012X}")
    print(f"XOR hex:  {int(mixed, 2):012X}")

    print("\n5. SPLITTING INTO EIGHT BLOCKS")
    print("Block | Output positions | E group | K group | B_j")
    for j, block in enumerate(blocks):
        start = j * 6
        print(f"B{j + 1}    | {start + 1:2d}-{start + 6:2d}            |"
              f" {expanded[start:start + 6]}  | {key[start:start + 6]}  | {block}")
    print("\nFINAL ANSWER")
    for j, block in enumerate(blocks, 1):
        print(f"B{j} = {block}")
    print("B1||B2||B3||B4||B5||B6||B7||B8 = " + mixed)
    print("These are the inputs to S1,...,S8, no S-box substitution is applied.")


def read_round():
    while True:
        value = input("Round i (1-16): ").strip()
        if value.isascii() and value.isdigit() and 1 <= int(value) <= 16:
            return int(value)
        print("Invalid round. Enter an integer from 1 to 16.")


def read_value(label, width, base):
    while True:
        try:
            return parse_value(input(label + ": "), width, base)
        except ValueError as error:
            print("Invalid input:", error)


def main():
    print("Laboratory 4: DES. n = 6, task = 6 mod 11 = 6 (2.6).")
    while True:
        print("\n1. Binary input\n2. Hexadecimal input\n3. Random input")
        print("4. Worked example (round 1)\n0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        if choice not in ("1", "2", "3", "4"):
            print("Choose 0, 1, 2, 3, or 4.")
            continue
        if choice == "4":
            round_number = 1
            right = format(0xF0AAF0AA, "032b")
            key = format(0x1B02EFFC7072, "048b")
        else:
            round_number = read_round()
            if choice == "3":
                right = format(secrets.randbits(32), "032b")
                key = format(secrets.randbits(48), "048b")
            else:
                base = 2 if choice == "1" else 16
                right = read_value("R_(i-1)", 32, base)
                key = read_value("K_i", 48, base)
        display_steps(right, key, round_number)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram ended.")
