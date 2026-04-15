# Code Fix Tool - API Hallucination Detector

A web application for detecting and fixing API hallucinations in LLM-generated code.

## Tech Stack

- **Frontend**: Vue 3 + Vite + TypeScript + Element Plus + Monaco Editor
- **Backend**: Python + FastAPI
- **State Management**: Pinia

## Project Structure

```
MidtermProject/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeEditor.vue    # Monaco Editor wrapper
│   │   │   ├── FixButton.vue     # Fix button component
│   │   │   └── FixStats.vue      # Statistics display
│   │   ├── store/
│   │   │   └── index.ts          # Pinia store
│   │   ├── App.vue               # Main layout
│   │   └── main.ts               # Entry point
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├── main.py                   # FastAPI server
│   └── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start the Backend Server

```bash
cd backend
python main.py
# Or use uvicorn directly:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

### 4. Start the Frontend Dev Server

```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:3000`

## Features

- **Left Panel**: Editable code editor (Monaco Editor) for inputting LLM-generated code
- **Right Panel**: Read-only code editor showing fixed code with highlighted corrections
- **Fix Button**: Trigger the fix API to detect and correct hallucinations
- **Auto-Fix Toggle**: Enable automatic fixing with debounce (1 second delay)
- **Statistics**: Display number of fixes and processing time
- **Fix Details**: Hover to view detailed fix information

## API Specification

### POST /fix

Detect and fix API hallucinations in the provided code.

**Request Body:**
```json
{
  "code": "import pands as pd\n..."
}
```

**Response:**
```json
{
  "fixed_code": "import pandas as pd\n...",
  "fixes": [
    {
      "line": 1,
      "column": 8,
      "original": "pands",
      "corrected": "pandas",
      "type": "package"
    }
  ],
  "status": "success"
}
```

## Detected Hallucination Types

The backend currently detects and fixes:

1. **Package Names**: Common misspellings like `pands` → `pandas`, `numppy` → `numpy`
2. **Function Names**: Typos like `prnt` → `print`, `lenght` → `len`
3. **Class Names**: Case issues like `Dataframe` → `DataFrame`, `Array` → `ndarray`

## Development

### Frontend Commands

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| GET | /health | Health status |
| POST | /fix | Fix code hallucinations |

## Screenshots

The application features:
- Clean, modern UI with gradient background
- Side-by-side code comparison
- Syntax highlighting with Monaco Editor
- Visual indicators for fixes (yellow highlight)
- Hover tooltips showing fix details

## License

MIT