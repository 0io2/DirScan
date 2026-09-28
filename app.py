import streamlit as st
import requests

st.title("🔍 Web Directory Scanner")

target_url = st.text_input("أدخل رابط الهدف:", "http://testphp.vulnweb.com")

if st.button("🚀 ابدأ الفحص الآن"):
    if not target_url:
        st.warning("الرجاء إدخال رابط الهدف أولاً!")
    else:
        # قائمة المسارات الأساسية مدمجة مباشرة لضمان العمل الفوري
        words = [
            "admin", "login", "robots.txt", "sitemap.xml", 
            "config.php", "index.php", "dashboard", "uploads", "test", "CGI-Bin"
        ]
        
        st.info(f"جاري فحص {len(words)} مساراً أساسياً على الهدف...")
        
        progress_bar = st.progress(0)
        status_box = st.empty()
        results_box = st.container()
        
        found = 0
        
        for i, word in enumerate(words):
            progress_bar.progress((i + 1) / len(words))
            status_box.text(f"جاري فحص المسار: /{word}")
            
            url = f"{target_url.rstrip('/')}/{word}"
            try:
                res = requests.get(url, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
                if res.status_code == 200:
                    found += 1
                    with results_box:
                        st.success(f"✅ متاح (200 OK): {url}")
                elif res.status_code == 403:
                    found += 1
                    with results_box:
                        st.warning(f"⚠️ محظور (403 Forbidden): {url}")
            except Exception as e:
                pass
        
        status_box.empty()
        progress_bar.empty()
        st.success(f"🎉 انتهى الفحص! إجمالي النتائج المكتشفة: {found}")