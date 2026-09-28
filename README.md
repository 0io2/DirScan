# DirScan 🛡️

A simple yet effective Python-based tool designed to scan web applications for sensitive paths, backup files, and configuration exposures (Information Disclosure vulnerabilities).

## 🚀 Features
- **Wordlist Support:** Reads paths dynamically from a custom wordlist (`common.txt`).
- **HTTP Status Handling:** Identifies accessible paths (`200 OK`) and protected paths (`403 Forbidden`).
- **Error Resilient:** Handles connection timeouts and exceptions smoothly without crashing the scan.

## 📋 Requirements
Make sure you have Python installed, then install the required `requests` library:
```bash
pip install requests