import requests
import os
import urllib3
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print_lock = threading.Lock()

def check_blocked(index, url):
    with print_lock:
        print(f"Scanning site {index + 1}: {url}")
    try:
        response = requests.get(url, timeout=10, verify=False)
        if (
            "This domain has been blocked" in response.text
            or "Web Page Blcked" in response.text
            or "The web page you are trying to visit has been blocked in accordance with school policy. Please contact your system administrator if you believe this is an error." in response.text
            or "Content Blocked" in response.text
            or "Certificate Error" in response.text
            or "This has been blocked by IT." in response.text
        ):
            return (url, True)
        return (url, False)
    except Exception as e:
        with print_lock:
            print(f"Error accessing {url}: {e}")
        return (url, True)

def main():
    blocked = []
    not_blocked = []
    with open("links.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    max_threads = max(4, os.cpu_count() or 4)
    print(f"Starting scan with {max_threads} threads based on system capabilities")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_blocked, i, url) for i, url in enumerate(urls)]
        for future in as_completed(futures):
            url, is_blocked = future.result()
            if is_blocked:
                blocked.append(url)
            else:
                not_blocked.append(url)

    print("\nBlocked URLs:")
    for url in blocked:
        print(url)
    print("\nNot Blocked URLs:")
    for url in not_blocked:
        print(url)

if __name__ == "__main__":
    main()