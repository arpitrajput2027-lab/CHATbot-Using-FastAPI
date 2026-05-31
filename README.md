# Sarvam AI Chatbot

A simple chatbot built with FastAPI + HTML/CSS/JS using [Sarvam AI](https://sarvam.ai).

---

## Folder Structure

```
sarvam-chatbot/
├── main.py
├── requirements.txt
├── .env
└── static/
    └── index.html
```

---

## Setup & Run

### 1. Clone the repo

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

```
SARVAM_API_KEY=your_api_key_here
```

> Sarvam API Key(Free): https://sarvam.ai

### 4. Run the server

```bash
uvicorn main:app --reload
```

### 5. Open in browser

```
http://localhost:8000
```

---

## Tech Stack

- **Backend** — FastAPI (Python)
- **Frontend** — HTML, CSS, JavaScript
- **AI Model** — Sarvam AI (`sarvam-m`)