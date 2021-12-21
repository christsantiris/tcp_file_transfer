import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected.")
    conn.send("OK@Welcome to the File Server".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        if cmd == "HELP":
            send_data = "OK@"
            send_data += "List: List all the files currently on the server.\n"
            send_data += "UPLOAD <path>: Upload files to the server.\n"
            send_data += "DELETE: <filename>: Delete a file from the server.\n"
            send_data += "LOGOUT: Disconnect from the server.\n"
            send_data += "HELP: List all the commands."

            conn.send(send_data.encode(FORMAT))
        elif cmd == "LOGOUT":
            break
        elif cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "There are no files on the server."
                conn.send(send_data.encode(FORMAT))
            else:
                send_data += "\n".join(f for f in files)
                conn.send(send_data.encode(FORMAT))
        elif cmd == "UPLOAD":
            pass
        elif cmd == "DELETE":
            pass

    print(f"[Disconnected] {addr} disconnected")

def main():
    print("[Starting] Server is starting.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
        server.listen()
    except socket.error as msg:
        print(f"Error socker.error {msg}")
        return

    print("[Listening] Server is listening")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
        main()