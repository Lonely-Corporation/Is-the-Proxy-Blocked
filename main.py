import requests

def check_blocked(url):
    try:
        response = requests.get(url, timeout=10)
        if "This domain has been blocked" in response.text:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return None

def main():
    blocked = []
    not_blocked = []
    with open("links.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    for url in urls:
        result = check_blocked(url)
        if result is True:
            blocked.append(url)
        elif result is False:
            not_blocked.append(url)
        else:
            print(f"ERROR: {url}")

    print("\nBlocked URLs:")
    for url in blocked:
        print(url)
    print("\nNot Blocked URLs:")
    for url in not_blocked:
        print(url)

if __name__ == "__main__":
    main()