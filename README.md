# 🛡 Web Vulnerability Scanner

A Python-based web security scanner with a **modern dark-themed GUI** built with Tkinter.  
Designed for **intermediate-level** students and educational/authorized penetration testing.

---

## ✨ Features

| Module | Description |
|---|---|
| 💉 SQL Injection | Error-based detection via URL params & forms |
| ⚡ XSS | Reflected Cross-Site Scripting detection |
| 🔒 Security Headers | Audits 7 security headers + 4 info-disclosure headers |
| 📁 Directory Traversal | Path traversal payload testing |
| ↪ Open Redirect | Detects unsafe URL redirect parameters |
| 📄 HTML Report | Auto-generated, dark-themed, severity-coloured report |
| 📊 JSON Export | Machine-readable findings export |

---

## 🗂 Project Structure

```
WebVulnScanner/
├── main.py              ← GUI entry point (run this)
├── scanner/
│   ├── __init__.py
│   ├── crawler.py       ← URL & form crawler
│   ├── sqli.py          ← SQL Injection scanner
│   ├── xss.py           ← XSS scanner
│   ├── headers.py       ← HTTP Security Headers auditor
│   ├── traversal.py     ← Directory Traversal scanner
│   └── redirect.py      ← Open Redirect scanner
├── report/
│   ├── __init__.py
│   └── generator.py     ← HTML & JSON report generator
├── reports/             ← Auto-saved HTML reports (created on first scan)
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

```bash
# 1. Navigate to the project folder
cd "d:\webvulnscan-project\WebVulnScanner"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the GUI
python main.py
```

---

## 🎯 How to Use

1. **Enter a target URL** in the Scanner tab (use a safe test target below)
2. **Select scan modules** to run (all enabled by default)
3. Set timeout and max pages in Advanced Options
4. Click **▶ Start Scan**
5. Watch the **Live Log** for real-time output
6. Switch to the **Results** tab to view findings by severity
7. Click a row to see **full details** in the detail panel
8. Use **Export HTML** or **Export JSON** to save your report

---

## ✅ Legal Test Targets (intentionally vulnerable)

> ⚠️ Always get written permission before scanning any system you don't own.

| Target | Description |
|---|---|
| `http://testphp.vulnweb.com` | Acunetix public demo — safe to test |
| `http://www.itsecgames.com` | bWAPP (run locally via Docker) |
| `http://dvwa.local` | DVWA (run locally via XAMPP / Docker) |

**Local DVWA setup:**
```bash
docker run -d -p 80:80 vulnerables/web-dvwa
# Then use: http://localhost
```

---

## ⚠️ Legal Disclaimer

This tool is for **educational purposes and authorized penetration testing ONLY**.  
Unauthorized scanning may violate the **Computer Fraud and Abuse Act (CFAA)**  
or equivalent laws in your jurisdiction.

**Never scan systems without explicit written permission from the owner.**

## Author

**Komalpreet Kaur**  
Cyber Security Trainee

This project was developed as part of my cybersecurity training to gain practical experience in web vulnerability assessment, security testing, and understanding common web application vulnerabilities.

**Purpose:** Learning, practice, and educational purposes.
