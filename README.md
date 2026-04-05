# 🛡️ Security Scanner Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A modern **AI-powered vulnerability scanner** with web dashboard, CVE integration and scan history.

---

## 🚀 Features

- ⚡ Async port scanning
- 🔍 Banner grabbing
- 🧠 Service detection
- 🛡️ CVE integration (NVD API)
- 🤖 AI-based vulnerability analysis
- 📊 Web dashboard
- 🗄️ Scan history
- ⚔️ Diff comparison

---

## 🖥️ Demo

Coming soon...

---

## ⚙️ Installation

```bash
git clone https://github.com/Murat666666/security-scanner.git
cd security-scanner
pip install -r requirements.txt
uvicorn api.main:app --reload

🌐 Usage

Open in browser:

http://127.0.0.1:8000

Example scan:

http://127.0.0.1:8000/scan?host=127.0.0.1&ports=22,80

## 🐧 CLI Usage

Run from terminal:

```bash
python cli/cli.py 127.0.0.1 22,80

Example output:

Port: 22
Service: openssh
AI: ⚠️ High risk!

## 🧠 Architecture

- API (FastAPI)
- Scanner Engine (Async)
- CVE Integration (NVD)
- AI Analysis Layer
- CLI Interface
- Web Dashboard

Render Server URL : https://security-scanner-murat.onrender.com
Usage : https://security-scanner-murat.onrender.com/scan?host=127.0.0.1&ports=22,80

# Security Scanner

AI-powered vulnerability scanner with web UI and CLI.

## Run locally


pip install -r requirements.txt
uvicorn api.main:app --reload


Open:
http://127.0.0.1:8000

## CLI


python cli/cli.py 127.0.0.1 22,80


## Deploy (Render)

Start command:

uvicorn api.main:app --host 0.0.0.0 --port $PORT
