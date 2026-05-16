# 🤖 CACE - Controlled AI Code Editor

**AI-powered code assistant that makes minimal, precise changes. No more full rewrites. No more hallucinations.**

---

## ✨ Features

- 🎯 **Intent-Driven Editing** - Tell it what you want, get only the necessary changes
- 🔍 **Diff-Based Updates** - See exactly what changes before applying
- ✅ **Syntax Validation** - Every change is validated before output
- 🔄 **Multi-LLM Fallback** - Automatic fallback for reliability (Gemini → Llama)
- ⚡ **Fast & Efficient** - Results in seconds
- 🎨 **Beautiful UI** - Glassmorphic design with black & white theme

---

## 📦 Project Structure

```
cace_project/
├── frontend/                 # HTML/CSS/JS frontend
│   ├── index.html           # Landing page
│   ├── get_started.html     # Editor interface
│   ├── style.css            # Glassmorphic styles
│   ├── javascript.js        # Frontend logic
│   └── file_*.png           # Assets
│
├── src/                     # Python backend
│   ├── llm.py              # LLM orchestration
│   ├── diff_engine.py      # Diff application logic
│   ├── analyzer.py         # Code validation
│   ├── models.py           # Pydantic models
│   └── treesitter_validationn.py              # for large project validation
│
├── server.py               # Flask API server
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
# Navigate to project directory
cd cace_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

**Required API Keys:**
- **Google API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Groq API Key** - Get from [Groq Console](https://console.groq.com/)

### 3. Run the Server

```bash
# Start the Flask backend
python server.py
```

You should see:
```
============================================================
🚀 CACE Backend Server Starting...
============================================================
📍 Frontend: http://localhost:5000
📍 API: http://localhost:5000/api
📍 Get Started: http://localhost:5000/get_started
============================================================
```

### 4. Open the App

Visit **http://localhost:5000** in your browser

---

## 🎮 How to Use

### Option 1: HTML Frontend (Recommended)

1. Visit `http://localhost:5000/get_started`
2. Paste your Python code in the **Source Code** box
3. Enter what you want to do in the **Prompt** box (or select a preset)
4. Click **Send** or press **Enter**
5. View the changes in the **Output** box
6. Check **Details** for change statistics and reasoning


## 📝 Example Usage

### Example 1: Fix Bugs

**Input Code:**
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

**Prompt:** `Fix potential bugs`

**Output:**
```python
def calculate_average(numbers):
    if not numbers:
        return 0
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

### Example 2: Add Type Hints

**Input Code:**
```python
def greet(name):
    return f"Hello, {name}!"
```

**Prompt:** `Add type hints`

**Output:**
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

---

## 🔧 API Endpoints

### `POST /api/process`

Process code with AI edits.

**Request:**
```json
{
  "source_code": "def hello():\n    print('Hello')",
  "prompt": "Add docstring"
}
```

**Response:**
```json
{
  "success": true,
  "modified_code": "...",
  "diffs": [...],
  "details": {
    "total_changes": 1,
    "total_lines": 2,
    "change_percentage": 50.0
  }
}
```

### `POST /api/validate`

Validate Python syntax.

**Request:**
```json
{
  "code": "def hello():\n    print('Hello')"
}
```

**Response:**
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": []
}
```

### `GET /api/presets`

Get available preset prompts.

**Response:**
```json
{
  "presets": [
    {
      "id": "optimize",
      "label": "🚀 Optimize Speed",
      "prompt": "Optimize this code for better performance"
    }
  ]
}
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/
```

---

## 🛠️ Development

### Project Components

**1. LLM Interface (`src/llm.py`)**
- Handles LLM orchestration
- Implements fallback mechanism (Gemini → Llama)
- Enforces structured output

**2. Diff Engine (`src/diff_engine.py`)**
- Applies code edits safely
- Handles line-by-line modifications
- Prevents index shifting issues

**3. Code Validator (`src/analyzer.py`)**
- AST-based syntax validation
- Error detection and reporting

**4. Flask Server (`server.py`)**
- REST API for frontend
- CORS enabled
- Error handling

**5. Frontend (`frontend/`)**
- Glassmorphic design
- Real-time code editing
- Diff visualization

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: API connection failed

**Solution:**
- Make sure `server.py` is running
- Check if port 5000 is available
- Verify `.env` file has valid API keys

### Issue: LLM not responding

**Solution:**
- Check your API keys in `.env`
- Verify internet connection
- Check API quota limits

---

## 🔐 Security Notes

- Never commit `.env` file with real API keys
- API keys are only stored locally
- No code is stored or transmitted except to LLM APIs

---

## 📚 Tech Stack

- **Backend:** Python, Flask, LangChain
- **Frontend:** HTML, TailwindCSS, Vanilla JavaScript
- **LLMs:** Google Gemini, Groq Llama
- **Validation:** Python AST
- **UI Framework (Alt):** Streamlit

---

## 🎯 Roadmap

### Phase 1 (Current) ✅
- Core diff engine
- Basic validation
- Single file editing
- Web interface

### Phase 2 (Next)
- Multi-file support
- Advanced validation (imports, types)
- History tracking
- Undo/redo functionality

### Phase 3 (Future)
- Memory graph for code structure
- IDE plugin (VS Code)
- Git integration
- Team collaboration

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📬 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/cace/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/cace/discussions)

---

## 🙏 Acknowledgments

Built with ❤️ using:
- LangChain for LLM orchestration
- Flask for API server
- TailwindCSS for styling
- Google Gemini & Groq for AI models

---

**Made by developers, for developers. Happy coding! 🚀**
