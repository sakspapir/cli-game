import tkinter as tk
from tkinter import scrolledtext
import threading
import os

class FakeFileSystem:
    def __init__(self):
        self.filesystem = {
            "root": {
                "type": "folder",
                "password": "",
                "contents": {
                    "folder1": {
                        "type": "folder",
                        "password": "",
                        "contents": {
                            "file1.txt": {
                                "type": "text",
                                "password": "",
                                "content": "Content of file1.txt"
                            },
                            "file2.txt": {
                                "type": "text",
                                "password": "",
                                "content": "Content of file2.txt"
                            }
                        }
                    },
                    "folder2": {
                        "type": "folder",
                        "password": "",
                        "contents": {
                            "file3.txt": {
                                "type": "text",
                                "password": "",
                                "content": "Content of file3.txt"
                            }
                        }
                    }
                }
            }
        }
        self.current_path = ["root"]

    def list_dir(self):
        current_dir = self.filesystem
        for folder in self.current_path:
            current_dir = current_dir["contents"]
        return current_dir.keys()

    def read_file(self, filename, password=""):
        current_dir = self.filesystem
        for folder in self.current_path:
            current_dir = current_dir["contents"]
        file = current_dir.get(filename)
        if file:
            if file["password"] and file["password"] != password:
                return "Incorrect password"
            return file["content"]
        return "File not found"

    def change_dir(self, foldername, password=""):
        if foldername == "..":
            if len(self.current_path) > 1:
                self.current_path.pop()
        else:
            current_dir = self.filesystem
            for folder in self.current_path:
                current_dir = current_dir["contents"]
            folder = current_dir.get(foldername)
            if folder and folder["type"] == "folder":
                if folder["password"] and folder["password"] != password:
                    return "Incorrect password"
                self.current_path.append(foldername)
            else:
                return "Directory not found"
        return "/".join(self.current_path)

    def get_path_completions(self, path):
        current_dir = self.filesystem
        for folder in self.current_path:
            current_dir = current_dir["contents"]
        return [item for item in current_dir.keys() if item.startswith(path)]

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulated Terminal")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black", cursor="none")  # Hide the mouse pointer
        self.fs = FakeFileSystem()

        font_settings = ("Courier", 24)  # Increase font size

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="black", fg="white", cursor="none", font=font_settings)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self.text_area.bind("<1>", self.refocus_entry)  # Refocus entry on text area click

        self.entry = tk.Entry(root, bg="black", fg="white", insertbackground="white", cursor="none", font=font_settings)
        self.entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.execute_command)
        self.entry.bind("<Tab>", self.autocomplete)
        self.entry.bind("<Up>", self.show_previous_command)
        self.entry.bind("<Down>", self.show_next_command)
        self.entry.focus_set()

        self.commands = ["ls", "cat", "cd", "exit"]
        self.command_history = []
        self.history_index = -1

        # Disable mouse events
        self.root.bind_all("<Button-1>", self.ignore_event)
        self.root.bind_all("<Button-2>", self.ignore_event)
        self.root.bind_all("<Button-3>", self.ignore_event)
        self.root.bind_all("<Motion>", self.ignore_event)

        # Configure tags for different text styles
        self.text_area.tag_config("folder", foreground="light blue")
        self.text_area.tag_config("file", foreground="light green")

    def ignore_event(self, event):
        return "break"

    def refocus_entry(self, event):
        self.entry.focus_set()
        return "break"

    def execute_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"> {command}\n")
        self.text_area.config(state=tk.DISABLED)
        self.scroll_to_end()
        if command == "exit":
            self.root.quit()
        else:
            if not self.command_history or self.command_history[-1] != command:
                self.command_history.append(command)
            self.history_index = len(self.command_history)
            threading.Thread(target=self.run_command, args=(command,)).start()
        self.entry.focus_set()

    def run_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            self.display_ls()
        elif cmd == "cat" and args:
            if len(args) == 2:
                output = self.fs.read_file(args[0], args[1])
            else:
                output = self.fs.read_file(args[0])
            self.display_output(output)
        elif cmd == "cd" and args:
            if len(args) == 2:
                output = self.fs.change_dir(args[0], args[1])
            else:
                output = self.fs.change_dir(args[0])
            self.display_output(output)
        else:
            output = "Command not found"
            self.display_output(output)

    def display_ls(self):
        current_dir = self.fs.filesystem
        for folder in self.fs.current_path:
            current_dir = current_dir["contents"]

        self.text_area.config(state=tk.NORMAL)
        for item in current_dir:
            if current_dir[item]["type"] == "folder":
                self.text_area.insert(tk.END, f"{item}\n", "folder")
            else:
                self.text_area.insert(tk.END, f"{item}\n", "file")
        self.text_area.config(state=tk.DISABLED)
        self.scroll_to_end()

    def display_output(self, output):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{output}\n")
        self.text_area.config(state=tk.DISABLED)
        self.scroll_to_end()

    def autocomplete(self, event):
        current_text = self.entry.get()
        if not current_text:
            return "break"

        parts = current_text.split()
        if len(parts) == 1:
            matches = [cmd for cmd in self.commands if cmd.startswith(parts[0])]
        else:
            matches = self.fs.get_path_completions(parts[-1])

        if matches:
            common_prefix = os.path.commonprefix(matches)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, " ".join(parts[:-1] + [common_prefix]))
        return "break"

    def show_previous_command(self, event):
        if self.command_history:
            self.history_index = max(0, self.history_index - 1)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])
        return "break"

    def show_next_command(self, event):
        if self.command_history:
            self.history_index += 1
            if self.history_index >= len(self.command_history):
                self.history_index = len(self.command_history)
                self.entry.delete(0, tk.END)
            else:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.command_history[self.history_index])
        return "break"

    def scroll_to_end(self):
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()
