import socket
import threading
from screen_receiver import ScreenReceiver
import tkinter as tk
class Server:
    def __init__(self, app):
        self.app = app
        self.server_thread = None
        self.server_running = False

    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.app.status_label.config(text="Status: Running")
            self.app.file_menu.entryconfig("Start Server", state=tk.DISABLED)
            self.app.file_menu.entryconfig("Stop Server", state=tk.NORMAL)
            self.server_thread = threading.Thread(target=self.run_server, args=(9999,))
            self.server_thread.start()

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.app.status_label.config(text="Status: Stopped")
            self.app.file_menu.entryconfig("Start Server", state=tk.NORMAL)
            self.app.file_menu.entryconfig("Stop Server", state=tk.DISABLED)

    def run_server(self, port):
        screen_receiver = ScreenReceiver(self.app)
        screen_receiver.receive_and_display_screen(port)
        self.stop_server()
