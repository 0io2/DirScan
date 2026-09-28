import requests
import os

def scan_target_generator(target_url, wordlist_path):
    """دالة مولدة (Generator) تعيد كل نتيجة فور اكتشافها للواجهة"""
    if target_url.endswith("/"):
        target_url = target_url[:-1]

    if not os.path.exists(wordlist_path):
        yield "error", f"خطأ: ملف التخمينات '{wordlist_path}' غير موجود!"
        return

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
        
        total = len(words)
        yield "info", total

        for i, word in enumerate(words):
            path = '/' + word if not word.startswith('/') else word
            url = target_url + path

            try:
                response = requests.get(url, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code == 200:
                    yield "found_200", url
                elif response.status_code == 403:
                    yield "found_403", url
            except requests.exceptions.RequestException:
                pass
            
            # إرسال التقدم أولاً بأول
            yield "progress", (i + 1, total)

    except Exception as e:
        yield "error", f"حدث خطأ أثناء قراءة الملف: {e}"