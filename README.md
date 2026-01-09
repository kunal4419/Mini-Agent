# Mini-Agent

A simple AI agent bot built with FastAPI and Google Gemini API.

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
```

## Running the Application

### Method 1: Web Chat Interface (Recommended)
```bash
bash run.sh
```
Then open your browser and navigate to:
- **Web Chat**: http://localhost:8000

### Method 2: Terminal Chat (CLI)
```bash
python3 chat_cli.py
```

### Method 3: Direct command (API Server)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Access the Application

- **Web Chat Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Send a message to the AI agent
- `GET /history` - Get chat history

## Project Structure

```
Mini-Agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   ├── agent.py         # AI agent logic
│   └── storage.py       # Simple in-memory storage
├── requirements.txt
├── run.sh
├── .env.example
└── README.md
```
