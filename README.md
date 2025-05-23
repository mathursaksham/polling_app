# Polling App

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up `.env` with your MySQL and SMTP credentials.

3. Run the app:
```bash
uvicorn app.main:app --reload --port 2544
```

4. Open `http://localhost:2544`
