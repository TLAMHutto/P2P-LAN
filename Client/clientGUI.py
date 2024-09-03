import tkinter as tk
from tkinter import messagebox
import pyautogui
import socket
import numpy as np
import pickle
import struct
import time
import threading

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")

        # Hard-coded server IP address
        self.server_ip = '192.168.0.19'
        self.server_port = 9999

        # Create and pack widgets
        tk.Label(root, text="Server IP Address:").pack(pady=5)
        tk.Label(root, text=self.server_ip).pack(pady=5)  # Display the hard-coded IP

        self.start_button = tk.Button(root, text="Start Sending", command=self.start_sending)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Sending", command=self.stop_sending, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Not sending")
        self.status_label.pack(pady=10)

        self.client_thread = None
        self.sending = False

    def start_sending(self):
        if not self.sending:
            self.sending = True
            self.status_label.config(text="Status: Sending")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.client_thread = threading.Thread(target=self.capture_and_send_screen)
            self.client_thread.start()

    def stop_sending(self):
        if self.sending:
            self.sending = False
            self.status_label.config(text="Status: Stopped")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def capture_and_send_screen(self, interval=5):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_ip, self.server_port))

            last_send_time = time.time()

            while self.sending:
                current_time = time.time()
                if current_time - last_send_time >= interval:
                    screenshot = pyautogui.screenshot()
                    frame = np.array(screenshot)
                    data = pickle.dumps(frame)
                    data_len = len(data)
                    sock.sendall(struct.pack("L", data_len))
                    sock.sendall(data)
                    last_send_time = current_time

                time.sleep(1)

        except Exception as e:
            print(f"[ERROR] Exception: {e}")

        finally:
            sock.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()