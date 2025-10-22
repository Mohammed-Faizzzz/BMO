def serialise_simple_string(string: str) -> str:
    return "+" + string + "\r\n"

def serialise_errors(error: Exception) -> str:
    return "-" + str(error) + "\r\n"

def serialise_int(number: int) -> str:
    return ":" + str(number) + "\r\n"

def serialise_bulk_string(string: str) -> str:
    NULL = "$-1\r\n"
    if string is None:
        return NULL
    res = "$"
    res += str(len(string))
    res += "\r\n"
    res += string
    res += "\r\n"
    return res

def serialise_arrays(arr: list) -> str:
    NULL = "*-1\r\n"
    if arr is None:
        return NULL

    res = "*"
    res += str(len(arr))
    res += "\r\n"
    
    for item in arr:
        if item is None:
            res += serialise_bulk_string(None)
        elif isinstance(item, str):
            res += serialise_bulk_string(item)
        elif isinstance(item, int):
            res += serialise_int(item)
        elif isinstance(item, list):
            res += serialise_arrays(item)
        elif isinstance(item, Exception):
            res += serialise_errors(item)
        else:
            raise TypeError("Unsupported type in array serialization")
    return res
    