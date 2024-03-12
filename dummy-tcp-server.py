import socket
import time

HOST = "0.0.0.0"
PORT = 5901

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server started, bound to {HOST}:{PORT}", flush=True)
    while True:
        print(f"Waiting for connections...", flush=True)
        try:
            conn, addr = s.accept()
            print(f"Connected by {addr}", flush=True)
            with conn:
                time.sleep(0.2)
                conn.sendall(b"RFB test\n")
                n = 0
                while True:
                    time.sleep(0.2)
                    n = n+1
                    conn.sendall(f"RFB broadcast {n}\n".encode())
        except:
            pass
