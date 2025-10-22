from main import (
    serialise_simple_string,
    serialise_errors,
    serialise_int,
    serialise_bulk_string,
    serialise_arrays,
    # deserialise,  # you’ll add later
)

def check(name, result, expected):
    status = "✅" if result == expected else f"❌ (got {result!r})"
    print(f"{name:25} {status}")

print("\n=== SIMPLE STRINGS ===")
check("simple OK", serialise_simple_string("OK"), "+OK\r\n")
check("simple hello", serialise_simple_string("hello world"), "+hello world\r\n")

print("\n=== ERRORS ===")
check("error msg", serialise_errors(Exception("Error message")), "-Error message\r\n")

print("\n=== INTEGERS ===")
check("int 42", serialise_int(42), ":42\r\n")

print("\n=== BULK STRINGS ===")
check("bulk ping", serialise_bulk_string("ping"), "$4\r\nping\r\n")
check("bulk empty", serialise_bulk_string(""), "$0\r\n\r\n")
check("bulk null", serialise_bulk_string(None), "$-1\r\n")

print("\n=== ARRAYS ===")
check("array single", serialise_arrays(["ping"]), "*1\r\n$4\r\nping\r\n")
check("array echo", serialise_arrays(["echo", "hello world"]), "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n")
check("array get key", serialise_arrays(["get", "key"]), "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n")

print("\n=== ROUND TRIP (later) ===")
print("(you’ll plug in deserialise() once you have it)")
