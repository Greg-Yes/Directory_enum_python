import requests
import time


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
            else:
                print(f"[-]Not found: {word}")
    except KeyboardInterrupt:
        print("Closing...")
    print("\nScan completed")


def main():
    url = "testphp.vulnweb.com"
    word_list = ["index", "login", "help", "faq", "testing3289759", "5454354665743"]
    
    banner()
    fixed_url = format_url(url)
    check_server(fixed_url)
    scan(fixed_url, word_list)


if __name__ == "__main__":
    main()
