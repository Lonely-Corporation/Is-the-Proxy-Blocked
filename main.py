import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_blocked(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        if "This domain has been blocked" in response.text:
            return (url, True)
        else:
            return (url, False)
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        # Treat any error as blocked
        return (url, True)

def main():
    blocked = []
    not_blocked = []
    with open("links.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_blocked, url) for url in urls]
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