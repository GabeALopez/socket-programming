#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Ayesha S. Dina

#Template used from author

import os
import socket
import threading

IP = "localhost"  ### gethostname()
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"


### to handle the clients
def handle_client(conn, addr):
    print(f"NEW CONNECTION: {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        if cmd == "LOGOUT":
            break

        elif cmd == "TASK":
            send_data += "LOGOUT from the server.\n"
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            file_name = data[1]
            receive_file(conn, file_name)

    print(f"{addr} disconnected")
    conn.close()


def receive_file(conn, file_name):
    try:
        directory_path = "Server_Path"
        file_path = os.path.join(directory_path, file_name)

        os.makedirs(directory_path, exist_ok=True)

        with open(file_path, "wb") as file:
            file_data = conn.recv(SIZE)
            while file_data:
                file.write(file_data)
                file_data = conn.recv(SIZE)
            print(f"File '{file_name}' received successfully.")
    except Exception as e:
        print(f"Error while received file: {str(e)}")


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## used IPV4 and TCP connection
    server.bind(ADDR)  # bind the address
    server.listen()  ## start listening
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept()  ### accept a connection from a client
        thread = threading.Thread(target=handle_client, args=(conn, addr))  ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()
