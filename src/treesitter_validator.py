from tree_sitter import Language, Parser
import tree_sitter_python as tsp
from models import ValidationResult 

class TreeSitterValidator:
    def __init__(self):
        # Initialize the Python grammar
        self.PY_LANGUAGE = Language(tsp.language())
        self.parser = Parser(self.PY_LANGUAGE)

    def get_all_errors(self, code_string) -> ValidationResult:
        """
        Parses the whole file and returns a list of ALL syntax errors.
        Never crashes on the first error!
        """
        tree = self.parser.parse(bytes(code_string, "utf8"))
        errors = []
        lines = code_string.split('\n')
        
        def traverse(node):
            # If the node is explicitly an error or a missing syntax element
            if node.type == 'ERROR' or node.is_missing:
                line_num = node.start_point[0] + 1  # Tree-sitter is 0-indexed
                
                # Avoid logging the exact same line error twice if it overlaps
                if not any(e['line'] == line_num for e in errors):
                    errors.append({
                        "line": line_num,
                        "description": "Syntax Error / Missing token",
                        "code_snippet": lines[line_num - 1].strip()
                    })
                    
            # Recursively check all child nodes in the tree
            for child in node.children:
                traverse(child)
                
        # Start walking the tree from the very top
        traverse(tree.root_node)
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=[])  

# --- Quick Test ---
if __name__ == "__main__":
    broken_code = """
def process_user_data(users, threshold
    valid_users = []
    
    for user in users:
        if user['age'] > threshold
            valid_users.append(user)
            
    config = {
        "max_retries": 5
        "timeout": 30
    }

    return valid_users
"""
    
    validator = TreeSitterValidator()
    all_errors = validator.get_all_errors(broken_code.strip('\n'))
    
    print("All Syntax Errors Found:")
    for error in all_errors.errors:
        print(f"Line {error['line']}: {error['description']}")
        print(f"  Code: {error['code_snippet']}\n") 