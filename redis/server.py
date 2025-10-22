import socket
from resp import deserialise, serialise_simple_string, serialise_bulk_string, serialise_int, serialise_arrays, serialise_errors
import asyncio

HOST = "127.0.0.1"
PORT = 6378

dictionary = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[Async] Client connected from {addr}")

    try:
        while True:
            data = await reader.read(1024)  # non-blocking
            if not data:
                break
            writer.write(data)              # echo back
            await writer.drain()            # wait until sent
    except Exception as e:
        print(f"[Async] Error with {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[Async] Client {addr} disconnected")

async def main():
    # HOST, PORT = "127.0.0.1", 6378
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[Async] Listening on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()
            
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
    
if __name__ == "__main__":
    asyncio.run(main())