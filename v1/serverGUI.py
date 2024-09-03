import tkinter as tk
from tkinter import messagebox
import socket
import cv2
import pickle
import numpy as np
import struct
import threading
from PIL import ImageGrab, ImageTk
from tkinter import filedialog
from datetime import datetime
import os
class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")

        # Create and pack the menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add "File" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Start Server", command=self.start_server)
        self.file_menu.add_command(label="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Add "Edit" menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Snip", command=self.start_snip)

        # Add "Help" menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        # Create and pack status label
        self.status_label = tk.Label(root, text="Status: Not running")
        self.status_label.pack(pady=10)

        # Create and pack image label for snipping tool
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.server_thread = None
        self.server_running = False

    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.status_label.config(text="Status: Running")
            self.file_menu.entryconfig("Start Server", state=tk.DISABLED)
            self.file_menu.entryconfig("Stop Server", state=tk.NORMAL)
            self.server_thread = threading.Thread(target=self.receive_and_display_screen, args=(9999,))
            self.server_thread.start()

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.status_label.config(text="Status: Stopped")
            self.file_menu.entryconfig("Start Server", state=tk.NORMAL)
            self.file_menu.entryconfig("Stop Server", state=tk.DISABLED)

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

    def show_about(self):
        messagebox.showinfo("About", "ServerApp v1.0\nA simple server application to display remote screen.")

    def start_snip(self):
        self.root.withdraw()
        self.snip_surface = tk.Toplevel(self.root)
        self.snip_surface.attributes("-fullscreen", True)
        self.snip_surface.attributes("-alpha", 0.3)
        self.snip_surface.configure(cursor="cross")

        self.canvas = tk.Canvas(self.snip_surface, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_snip_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        self.snip_surface.withdraw()
        self.root.deiconify()

        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.show_image(image)

        self.snip_surface.destroy()

    def show_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        # Define the save directory
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
        
        if save_dir:
            # Use a fixed filename to overwrite previous file
            filename = "snip_latest.png"
            
            # Create the full file path
            file_path = os.path.join(save_dir, filename)
            
            # Ensure the save directory exists
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Save the image
            image.save(file_path)
            
            messagebox.showinfo("Image Saved", f"Image saved as {filename} in {save_dir}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()