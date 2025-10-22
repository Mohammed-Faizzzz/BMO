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

def deserialise(data: str):
    if not data:
        raise ValueError("No data to deserialise")
    elif data.startswith("+"): # Simple String
        return data[1:-2]
    elif data.startswith("-"):
        return Exception(data[1:-2])
    elif data.startswith(":"):
        return int(data[1:-2])
    elif data.startswith("$"):
        length = int(data[1:data.index("\r\n", 1)])
        if length == -1:
            return None
        return data[data.index("\r\n", 1) + 2:data.index("\r\n", data.index("\r\n", 1) + 2)]
    elif data.startswith("*"):
        items = data[1:-2].split("\r\n")
        return [deserialise(item) for item in items if item]
    else:
        raise ValueError("Unknown RESP type")    