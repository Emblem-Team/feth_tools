ESC_PAIR = [("\u001b", "$")]


def escape_str(string: str) -> str:
    for pair in ESC_PAIR:
        string = string.replace(*pair)
    return string


def scape_str(string: str) -> str:
    string = "\n".join(string.splitlines())
    for pair in ESC_PAIR:
        string = string.replace(pair[1], pair[0])
    return string
