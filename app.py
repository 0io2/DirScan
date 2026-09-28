import streamlit as st
import requests

st.title("🔍 Web Directory Scanner")

target_url = st.text_input("أدخل رابط الهدف:", "http://testphp.vulnweb.com")

if st.button("ابدأ الفحص"):
    st.write("جاري الفحص...")
    try:
        with open("common.txt", "r") as f:
            words = f.read().splitlines()
        
        found = []
        for word in words:
            word = word.strip()
            if not word:
                continue
            url = f"{target_url.rstrip('/')}/{word}"
            try:
                res = requests.get(url, timeout=2)
                if res.status_code == 200:
                    found.append(url)
            except:
                pass
        
        st.success("انتهى الفحص!")
        for p in found:
            st.write(p)
            
    except FileNotFoundError:
        st.error("ملف common.txt غير موجود!")