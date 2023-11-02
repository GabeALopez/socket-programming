#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Ayesha S. Dina

#Template used from author

import os
import socket

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024  ## byte .. buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    while True:  ### multiple communications
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "UPLOAD":
            file_path = data[1]
            upload_file(client, file_path)
        elif cmd == "DELETE":
            file_name = data[1]
            client.send(f"DELETE@{file_name}".encode(FORMAT))
            print("Sent delete command")

    print("Disconnected from the server.")
    client.close()  ## close the connection


def upload_file(client, file_path):
    try:
        file_name = os.path.basename(file_path)
        client.send(f"UPLOAD@{file_name}".encode(FORMAT))

        with open(file_name, "rb") as file:
            file_data = file.read(SIZE)
            while file_data:
                client.send(file_data)
                file_data = file.read(SIZE)
            print(f"File '{file_name}' uploaded successfully.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found")
    except Exception as e:
        print(f"Error while sending file: {str(e)}")


if __name__ == "__main__":
    main()
