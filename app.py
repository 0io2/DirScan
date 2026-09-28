import streamlit as st
import requests
import os

st.title("🔍 Web Directory Scanner - Full Wordlist")

target_url = st.text_input("أدخل رابط الهدف:", "http://testphp.vulnweb.com")
wordlist_file = "common.txt"

if st.button("🚀 ابدأ الفحص الشامل"):
    if not target_url:
        st.warning("الرجاء إدخال رابط الهدف أولاً!")
    elif not os.path.exists(wordlist_file):
        st.error(f"خطأ: ملف التخمينات '{wordlist_file}' غير موجود في المستودع!")
    else:
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            
            total = len(words)
            st.info(f"تم تحميل الملف بنجاح! جاري فحص {total} مساراً...")
            
            progress_bar = st.progress(0)
            status_box = st.empty()
            results_box = st.container()
            
            found = 0
            
            for i, word in enumerate(words):
                progress_bar.progress((i + 1) / total)
                status_box.text(f"جاري الفحص ({i+1}/{total}): /{word}")
                
                path = '/' + word if not word.startswith('/') else word
                url = target_url.rstrip('/') + path
                
                try:
                    res = requests.get(url, timeout=2, headers={"User-Agent": "Mozilla/5.0"})
                    if res.status_code == 200:
                        found += 1
                        with results_box:
                            st.success(f"✅ [200 OK] {url}")
                    elif res.status_code == 403:
                        found += 1
                        with results_box:
                            st.warning(f"⚠️ [403 Forbidden] {url}")
                except requests.exceptions.RequestException:
                    pass
            
            status_box.empty()
            progress_bar.empty()
            st.success(f"🎉 انتهى الفحص الشامل! إجمالي النتائج المكتشفة: {found}")
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")