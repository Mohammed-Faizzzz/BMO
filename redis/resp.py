
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
        return None

    prefix = data[0]

    # Simple String
    if prefix == '+':
        return data[1:data.index("\r\n")]

    # Error
    elif prefix == '-':
        return Exception(data[1:data.index("\r\n")])

    # Integer
    elif prefix == ':':
        return int(data[1:data.index("\r\n")])

    # Bulk String
    elif prefix == '$':
        end_of_len = data.index("\r\n")
        length = int(data[1:end_of_len])
        if length == -1:
            return None
        start = end_of_len + 2
        end = start + length
        return data[start:end]

    # Array
    elif prefix == '*':
        end_of_count = data.index("\r\n")
        count = int(data[1:end_of_count])
        if count == -1:
            return None

        items = []
        i = end_of_count + 2
        for _ in range(count):
            prefix = data[i]
            if prefix == '$':
                end_of_len = data.index("\r\n", i)
                length = int(data[i + 1:end_of_len])
                if length == -1:
                    items.append(None)
                    i = end_of_len + 2
                else:
                    start = end_of_len + 2
                    end = start + length
                    items.append(data[start:end])
                    i = end + 2
            else:
                raise ValueError(f"Unsupported nested type {prefix!r}")

        return items

    else:
        raise ValueError(f"Unknown RESP type {prefix!r}")
