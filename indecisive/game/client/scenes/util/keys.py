import string


def arcade_int_to_string(key: int, mod: int) -> str:
    if 97 <= key <= 122:
        if (mod & 1) == 1:
            return string.ascii_uppercase[key-97]
        else:
            return string.ascii_lowercase[key-97]
    elif 48 <= key <= 57:
        return str(key - 48)
    elif 65456 <= key <= 65465:
        return str(key - 65456)
    elif 58 <= key <= 64 or 91 <= key <= 96 or 123 <= key <= 126 or 32 <= key <= 47:
        return chr(key)
    else:
        return ""
