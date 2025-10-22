import socket
from resp import deserialise, serialise_simple_string, serialise_bulk_string, serialise_int, serialise_arrays, serialise_errors

HOST = "127.0.0.1"
PORT = 6378

dictionary = {}

def start_server():
    """
    start server on TCP socket to listen to incoming redis commands and respond accordingly
    """
    print(f"Starting Redis Lite on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print("Listening for connections...")

        while True:
            conn, addr = server.accept()
            print(f"Client connected from {addr}")
            with conn:
                buffer = ""
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    buffer += data.decode()
                    # Try parsing one command at a time
                    # check if buffer is a string
                    print(isinstance(buffer, str), buffer[0])
                    cmd = deserialise(buffer)
                    if cmd is not None:
                        response = handle_command(cmd)
                        conn.sendall(response.encode())
                        buffer = ""  # reset for next command

def handle_command(cmd):
    # cmd will be like ["PING"] or ["ECHO", "Hello World"]
    global dictionary
    if not cmd:
        return serialise_simple_string("")

    command = cmd[0].upper()

    if command == "PING":
        # reply with PONG
        return serialise_simple_string("PONG")

    elif command == "ECHO":
        if len(cmd) >= 2:
            return serialise_bulk_string(cmd[1])
        else:
            return serialise_bulk_string("")
    elif command == "SET":
        if len(cmd) >= 3:
            key = cmd[1]
            value = cmd[2]
            dictionary[key] = value
            return serialise_simple_string("OK")
        else:
            return serialise_errors(Exception("ERR wrong number of arguments for 'SET' command"))
    elif command == "GET":
        if len(cmd) >= 2:
            key = cmd[1]
            value = dictionary.get(key, None)
            return serialise_bulk_string(value)
        else:
            return serialise_errors(Exception("ERR wrong number of arguments for 'GET' command"))
    elif command == "CHECK":
        return serialise_arrays(list(dictionary.keys()) + list(dictionary.values()))
    else:
        return serialise_bulk_string(f"Unknown command {command}")
    

start_server()