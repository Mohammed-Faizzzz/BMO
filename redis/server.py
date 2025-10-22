import socket
from resp import deserialise, serialise_simple_string, serialise_bulk_string, serialise_int, serialise_arrays, serialise_errors
import threading

HOST = "127.0.0.1"
PORT = 6378

dictionary = {}

def handle_client(conn, addr):
    print(f"Client connected from {addr}")
    buffer = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode()

            cmd = deserialise(buffer)
            if cmd:
                response = handle_command(cmd)
                conn.sendall(response.encode())
                buffer = ""
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"Client {addr} disconnected")


def start_server():
    HOST = "127.0.0.1"
    PORT = 6378
    print(f"Starting Redis Lite on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print("Listening for connections...")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
            
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
        pairs = [[k, v] for k, v in dictionary.items()]
        print(pairs)
        return serialise_arrays([serialise_arrays(pair) for pair in pairs])
    else:
        return serialise_errors(Exception(f"ERR unknown command '{command}'"))
    

start_server()