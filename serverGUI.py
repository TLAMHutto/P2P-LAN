import tkinter as tk
from tkinter import messagebox
import socket
import cv2
import pickle
import numpy as np
import struct
import threading

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")

        # Create and pack widgets
        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Not running")
        self.status_label.pack(pady=10)

        self.server_thread = None
        self.server_running = False

    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.status_label.config(text="Status: Running")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.server_thread = threading.Thread(target=self.receive_and_display_screen, args=(9999,))
            self.server_thread.start()

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.status_label.config(text="Status: Stopped")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def receive_and_display_screen(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.listen(5)

            conn, addr = sock.accept()

            while self.server_running:
                try:
                    data_len = struct.unpack("L", conn.recv(4))[0]
                    data = b''
                    while len(data) < data_len:
                        chunk = conn.recv(4096)
                        if not chunk:
                            return
                        data += chunk
                    frame = pickle.loads(data)
                    cv2.imshow('Laptop Screen', frame)
                    if cv2.waitKey(1) == ord('q'):
                        break
                except Exception as e:
                    print(f"[ERROR] Exception: {e}")
                    break

            conn.close()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"[ERROR] Exception: {e}")

        finally:
            self.stop_server()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
