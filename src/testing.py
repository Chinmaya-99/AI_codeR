from llm import llminit
from analyzer import CodeValidator
from diff_engine import DiffEngine
from models import CodeDiff
from treesitter_validator import TreeSitterValidator

# =========================================================
# 1. USER INPUT (manual for now)
# =========================================================

intent = "Fix the syntax error in the function"
#test data with multiple syntax errors to test the robustness of the system.
target_code1 = """
def calculate_total(price, tax
    total = price + (price * tax)

    if total > 100
        print("Large order")

     return total


def greet(name):
    print("Hello " + name

numbers = [1, 2, 3

for n in numbers:
print(n)
"""
target_code = """
import json
from datetime import datetime

class OrderProcessor
    def __init__(self, api_key, region="US"):
        self.api_key = api_key
        self.region = region
        self.cache = {}

    def fetch_orders(self, status="pending"
        print(f"Fetching {status} orders...")
        
        payload = {
            "api_key": self.api_key
            "status": status,
            "limit": 100
        }
        
        if not self.api_key
            raise ValueError("API Key is missing")
            
        mock_data = [{"id": 1, "total": 250}, {"id": 2, "total": 45.5}
        
        try:
            data = mock_data
        except Exception as e
            print(f"Error processing data: {e}")
            return []
            
        return data

    def calculate_revenue(self, orders):
        total_revenue = 0
        
        for order in orders:
            if order.get('total', 0) > 0:
                total_revenue += order['total']
                
        return total_revenue

# Execution
processor = OrderProcessor("secret_key_123")
orders = processor.fetch_orders()
revenue = processor.calculate_revenue(orders
print(f"Total Revenue: ${revenue}")
"""
target_code = target_code.strip('\n')

target_code = target_code.strip("\n")
print("\n========== USER INPUT ==========\n")
print("Intent:")
print(intent)

print("\nTarget Code:")
print(target_code)

# =========================================================
# 2. INITIAL ANALYSIS
# =========================================================
validator= TreeSitterValidator()
initial_analysis = validator.get_all_errors(target_code)

print("\n========== INITIAL ANALYSIS ==========\n")
print("All Syntax Errors Found:")
for error in initial_analysis.errors:
    print(f"Line {error['line']}: {error['description']}")
    print(f"  Code: {error['code_snippet']}\n") 
# =========================================================
# 3. LLM DIFF GENERATION
# =========================================================

engine = llminit()

print("\n========== NUMBERING TARGEET CODE LINE ==========\n")
def format_with_lines(code_string):
    """Adds line numbers to the code so the LLM stops guessing."""
    lines = code_string.split('\n')
    return '\n'.join([f"{i+1:3} | {line}" for i, line in enumerate(lines)])
formated_code = format_with_lines(target_code)
print("\nFormated Target Code with Line Numbers:")
print(formated_code)  

print("\n========== FORMATED ERRORS ==========\n")
# Create a highly readable string of the entire error map
formated_errors = ""
for err in initial_analysis.errors:
    formated_errors += f"- Line {err['line']}: {err['description']} (Snippet: `{err['code_snippet']}`)\n"
print(formated_errors) 


diff_response = engine.get_edits(
    intent=intent,
    target_code=formated_code,
    formatted_errors=formated_errors)

print("\n========== GENERATED DIFF ==========\n")
print(diff_response)


# =========================================================
# 4. APPLY DIFF
# =========================================================
engine = DiffEngine()
updated_code = engine.apply_edits(target_code,diff_response.diffs)

print("\n========== PATCHED CODE ==========\n")
print(updated_code)


# =========================================================
# 5. FINAL ANALYSIS
# =========================================================

final_analysis = TreeSitterValidator().get_all_errors(updated_code) 

print("\n========== FINAL ANALYSIS ==========\n")
print(final_analysis)


# =========================================================
# 6. FINAL RESULT
# =========================================================

if final_analysis.is_valid:
    print("\n✅ Code successfully fixed.")
else:
    print("\n❌ Code still contains errors.")