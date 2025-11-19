import requests
import time
import argparse


HEADERS = {"User-Agent": "Mozilla/5.0 (Xll; Linux x86_64)"}
TIMEOUT = 10

def banner():
    print("-" * 65)
    print("\nHi and welcome to my directory enumeration tool based on python\n")
    print("-" * 65)
    time.sleep(1)

def format_url(link: str) -> str:
    if not link.startswith("http://"):
        link = "http://" + link
    if not link.endswith("/"):
        link = link + "/"
    return link

def check_server(link: str):
    resp = requests.get(link, timeout=TIMEOUT, headers=HEADERS)
    try:
        if resp.status_code == 200:
            print(f"\n[+] Host URL : {link}")
            print(f"[+] Status   : {resp.status_code}")
            print(f"[+] Server   : {resp.headers.get('Server', 'Unknown')}")
            print(f"[+] Title    : {resp.text.split('<title>')[1].split('</title>')[0] if '<title>' in resp.text else 'N/A'}\n")
            print("-" * 65)
    except KeyboardInterrupt:
        print("Closing")
    except Exception as e:
        print(f"Unexpected error has occured: {e}")

def scan(url: str, wordlist: str):
    s = requests.Session()
    try:
        for word in wordlist:
            session = s.get(url, timeout=TIMEOUT)
            if session.status_code == 200:
                print(f"[+] Found: {word}")
    except KeyboardInterrupt:
        print("Closing...")
    print("\nScan completed")


def main():
    parser = argparse.ArgumentParser(description="Simple python directory enumeration tool")
    
    parser.add_argument("-u", help="Target url or IP address. e.g. http://example.com")
    parser.add_argument("-w", help="Path to wordlist")

    args = parser.parse_args()

    with open(args.w, "r") as l:
        words = [line.strip() for line in l if line.strip()]

    banner()
    fixed_url = format_url(args.u)
    check_server(fixed_url)
    scan(fixed_url, words)


if __name__ == "__main__":
    main()
