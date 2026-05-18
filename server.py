from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))  # Ensure we can import from src/

from src.treesitter_validator import TreeSitterValidator
from src.llm import llminit
from src.diff_engine import DiffEngine

# ============================================================================
# 1. APP INITIALIZATION & CONFIGURATION
# ============================================================================
# We point Flask to serve static files (HTML/CSS/JS) straight from your frontend folder
app = Flask(__name__, static_folder='ui', static_url_path='')
CORS(app) # Enables Cross-Origin Resource Sharing (allows frontend to talk to API)

print("Initializing CACE AI Engine components...")
llm_engine = llminit()
validator = TreeSitterValidator()
diff_engine = DiffEngine()

# ============================================================================
# 2. UTILITY FUNCTIONS
# ============================================================================
def format_with_lines(code_string):
    """Adds precise visual line numbers to code to anchor the LLM."""
    lines = code_string.split('\n')
    return '\n'.join([f"{i+1:3} | {line}" for i, line in enumerate(lines)])

# ============================================================================
# 3. FRONTEND STATIC ROUTES
# ============================================================================
@app.route('/')
def index():
    """Serves the main landing page"""
    return send_from_directory('ui', 'index.html')

@app.route('/get_started')
def get_started():
    """Serves the code editor UI"""
    return send_from_directory('ui', 'get_started.html')

# ============================================================================
# 4. API ROUTES (The Nervous System)
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Validates that the backend is awake and listening."""
    return jsonify({"status": "ok", "message": "CACE Backend is fully operational!"})

@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Provides the Dropdown preset options to the Javascript UI."""
    return jsonify({
        "presets": [
            {"id": "optimize", "label": "🚀 Optimize Speed", "prompt": "Optimize this code for better performance. Ensure minimal diffs."},
            {"id": "fix_bugs", "label": "🐛 Fix Bugs", "prompt": "Fix all syntax and logical errors in this code."},
            {"id": "comments", "label": "📝 Add Comments", "prompt": "Add detailed, professional docstrings and inline comments."},
            {"id": "type_hints", "label": "🏷️ Add Type Hints", "prompt": "Add Python type hints to all function arguments and return types."}
        ]
    })

@app.route('/api/process', methods=['POST'])
def process_code():
    """
    THE MASTER PIPELINE:
    This endpoint catches the code from the UI, runs it through the analyzer,
    queries the LLM, applies the patches via the engine, and sends the result back.
    """
    try:
        # 1. Catch the data from the Frontend (javascript.js)
        data = request.json
        source_code = data.get('source_code', '')
        user_intent = data.get('prompt', '')

        if not source_code.strip():
            return jsonify({"success": False, "error": "No source code provided."}), 400

        print(f"\n[API] Received request: '{user_intent}'")

        # 2. TREE-SITTER ANALYZER: Find all syntax errors without crashing
        analysis = validator.get_all_errors(source_code)
        
        # Format the errors into a readable map for the LLM
        formatted_errors = "No syntax errors found by parser.\n"
        if not analysis.is_valid:
            formatted_errors = ""
            for err in analysis.errors:
                formatted_errors += f"- Line {err['line']}: {err['description']} (Snippet: `{err['code_snippet']}`)\n"

        # 3. PREPARE THE PAYLOAD: Number the code
        numbered_code = format_with_lines(source_code)

        print("[API] Routing error payload to LLM...")

        # 4. INVOKE LLM: Send the prompt, the numbered code, and the error map
        # Note: We call 'final_chain.invoke' directly to strictly enforce our payload
        diff_response = llm_engine.final_chain.invoke({
            "intent": user_intent,
            "code": numbered_code,
            "analysis": formatted_errors
        })

        # Extract the list of CodeDiff objects from the Pydantic wrapper
        generated_diffs = diff_response.diffs
        
        print(f"[API] LLM generated {len(generated_diffs)} operations. Applying...")

        # 5. DIFF ENGINE: Apply the patches bottom-up to the RAW code
        patched_code = diff_engine.apply_edits(source_code, generated_diffs)

        # 6. CALCULATE UI METRICS: Gather stats for the frontend dashboard
        total_lines = len(source_code.split('\n'))
        total_changes = len(generated_diffs)
        
        # Calculate rough percentage of the file modified
        lines_changed = sum(1 for d in generated_diffs if d.operation in ['replace', 'delete']) + \
                        sum(len(d.new_code.split('\n')) for d in generated_diffs if d.new_code)
        
        change_percentage = 0
        if total_lines > 0:
            change_percentage = round(min((lines_changed / total_lines) * 100, 100), 1)

        # 7. SERIALIZE: Convert Pydantic objects to standard dictionaries for JSON
        serialized_diffs = []
        for d in generated_diffs:
            serialized_diffs.append({
                "operation": d.operation,
                "start_line": d.start_line,
                "end_line": d.end_line,
                "new_code": d.new_code,
                "reasoning": d.reasoning
            })

        print("[API] Successfully processed request. Sending to client.")

        # 8. RESPOND: Send everything back to the glassmorphic UI!
        return jsonify({
            "success": True,
            "modified_code": patched_code,
            "diffs": serialized_diffs,
            "details": {
                "total_changes": total_changes,
                "total_lines": total_lines,
                "change_percentage": change_percentage
            }
        })

    except Exception as e:
        print(f"\n[API ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# 5. SERVER EXECUTION
# ============================================================================
if __name__ == '__main__':
    print("============================================================")
    print("🚀 CACE Backend Server Starting...")
    print("📍 Frontend: http://localhost:5000")
    print("📍 Editor UI: http://localhost:5000/get_started")
    print("============================================================")
    # Install 'flask' and 'flask-cors' via pip if you haven't already!
    app.run(debug=True, port=5000)