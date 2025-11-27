import requests
import time
import argparse
import threading
#from queue import Queue


HEADERS = {"User-Agent": "Mozilla/5.0 (Xll; Linux x86_64)"}
TIMEOUT = 10

def banner():
    print("-" * 65)
    print("\nHi and welcome to my directory enumeration tool based on python\n")
    print("-" * 65)

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
    baseline = s.get(url).content
    baseline_size = len(baseline)

    for word in wordlist:
        try:
            session = s.get(url, timeout=TIMEOUT, allow_redirects=True)
            size = len(session.content)

            if abs(size - baseline_size) < 50:
                continue

            if session.status_code in (200, 301, 302, 404):
                print(f"[+] Found: {word}")

                if session.status_code == 403:
                    print("Forbidden: {word} - Very interesting")

        except requests.exceptions.RequestException:
            pass
        except KeyboardInterrupt:
            print("Closing...")

    print("\nScan completed")


def main():
    parser = argparse.ArgumentParser(description="Simple python directory enumeration tool")
    
    parser.add_argument("-u", help="Target url or IP address. e.g. http://example.com", required=True)
    parser.add_argument("-w", help="Path to wordlist", required=True)
    parser.add_argument("-t", help="Number of threads (default: 10)", type=int, default=10)

    args = parser.parse_args()

    banner()
    time.sleep(1)
    fixed_url = format_url(args.u)
    check_server(fixed_url)

    with open(args.w, "r") as l:
        words = [line.strip() for line in l if line.strip()]
    
    threads = []
    try:
        for _ in range(args.t):
            t = threading.Thread(target=scan, args=(fixed_url, words))
            t.daemon = True
            t.start()
            threads.append(t)
    
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Closing...")
    

if __name__ == "__main__":
    main()
