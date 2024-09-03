import tkinter as tk
from tkinter import messagebox
from server import Server
from snip_tool import SnipTool
from image_handler import ImageHandler

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")

        self.server = Server(self)
        self.snip_tool = SnipTool(self)
        self.image_handler = ImageHandler(self)

        # Create and pack the menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add "File" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Start Server", command=self.server.start_server)
        self.file_menu.add_command(label="Stop Server", command=self.server.stop_server, state=tk.DISABLED)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Add "Edit" menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Snip", command=self.snip_tool.start_snip)

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

    def show_about(self):
        messagebox.showinfo("About", "ServerApp v1.0\nA simple server application to display remote screen.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
