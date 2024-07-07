from colorama import *
import requests
import random
from concurrent.futures import ThreadPoolExecutor
from src.core import print_with_timestamp, print_line, countdown_timer
from src.core import mrh, hju, htm , kng, pth, bru, reset

class Proxy:
    def __init__(self):
        self.proxy_sources = [
            'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=text&timeout=20000',
            'https://www.proxy-list.download/api/v1/get?type=http',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
        ]
        self.proxies_file = './data/proxies.txt'
        self.workers = 10  # Number of worker threads

    def get_proxies(self):
        all_proxies = []

        for url in self.proxy_sources:
            try:
                response = requests.get(url)
                proxies = response.text.strip().split('\n')
                all_proxies.extend(proxies)
            except requests.RequestException as e:
                print_with_timestamp(f"{mrh}Failed to fetch proxies from {url}. Error: {e}")

        all_proxies = list(set(all_proxies))  # Remove duplicates
        all_proxies.sort()

        with open(self.proxies_file, 'w') as file:
            for index, proxy in enumerate(all_proxies, start=1):
                file.write(f"{proxy}\n")
            print_with_timestamp(f"{hju}Found a total {pth}{index} {hju}proxies ")

        return all_proxies

    def is_proxy_live(self, proxy):
        url = 'http://httpbin.org/ip'
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                return True
        except requests.RequestException:
            return False

    def get_random_proxy(self):
        with open(self.proxies_file, 'r') as file:
            proxies = file.read().strip().split('\n')
        return random.choice(proxies)
    
    def remove_dead_proxies(self, dead_proxies):
        with open(self.proxies_file, 'r') as file:
            proxies = file.readlines()

        with open(self.proxies_file, 'w') as file:
            for proxy in proxies:
                if proxy.strip() not in dead_proxies:
                    file.write(proxy)

    def get_live_proxies(self):
        with open(self.proxies_file, 'r') as file:
            proxies = file.read().strip().split('\n')

        live_proxies = []
        dead_proxies = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = list(executor.map(self.is_proxy_live, proxies))

        for proxy, is_live in zip(proxies, results):
            if is_live:
                live_proxies.append(proxy)
            else:
                dead_proxies.append(proxy)

        self.remove_dead_proxies(dead_proxies)

        return live_proxies
