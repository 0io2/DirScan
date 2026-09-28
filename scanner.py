import requests
import sys
from datetime import datetime
import os

def scan_target(target_url, wordlist_path):
    print("=" * 60)
    print(f"[*] Starting Information Disclosure Scan on: {target_url}")
    print(f"[*] Using Wordlist: {wordlist_path}")
    print(f"[*] Time started: {datetime.now()}")
    print("=" * 60)

    # التأكد من أن الرابط ينتهي بـ / أو لا
    if target_url.endswith("/"):
        target_url = target_url[:-1]

    # التأكد من وجود ملف التخمينات
    if not os.path.exists(wordlist_path):
        print(f"[X] Error: The wordlist file '{wordlist_path}' was not found!")
        sys.exit(1)

    found_paths = 0
    tested_paths = 0

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            for line in file:
                path = line.strip()
                # تجاهل الأسطر الفارغة أو التعليقات
                if not path or path.startswith('#'):
                    continue

                # التأكد من أن المسار يبدأ بـ /
                if not path.startswith('/'):
                    path = '/' + path

                url = target_url + path
                tested_paths += 1

                try:
                    # إرسال طلب GET للموقع
                    response = requests.get(url, timeout=5)
                    
                    # إذا كان الرد 200 (يعني الملف أو الصفحة موجودة ومكشوفة)
                    if response.status_code == 200:
                        print(f"[+] [FOUND - 200 OK] {url}")
                        found_paths += 1
                    # إذا كان الرد 403 (ممنوع الوصول ولكنها تدل على وجود المسار)
                    elif response.status_code == 403:
                        print(f"[!] [FORBIDDEN - 403] {url}")
                    
                except requests.exceptions.RequestException:
                    continue

    except Exception as e:
        print(f"[X] An error occurred while reading the wordlist: {e}")
        sys.exit(1)

    print("=" * 60)
    print(f"[*] Scan completed.")
    print(f"[*] Total paths tested: {tested_paths}")
    print(f"[*] Accessible sensitive paths found: {found_paths}")
    print("=" * 60)

if __name__ == "__main__":
    target = input("Enter target URL (e.g., http://example.com): ").strip()
    wordlist = input("Enter your wordlist filename (e.g., common.txt): ").strip()
    
    if target and wordlist:
        scan_target(target, wordlist)
    else:
        print("[X] Please provide both a target URL and a wordlist file.")