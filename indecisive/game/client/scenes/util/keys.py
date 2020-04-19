import string


def arcade_int_to_string(key: int, mod: int) -> str:
    print(key)
    if 97 <= key <= 122:
        if mod & 1 == 1:
            return string.ascii_uppercase[key-97]
        else:
            return string.ascii_lowercase[key-97]
    else:
        return ""
