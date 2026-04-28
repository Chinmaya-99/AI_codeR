# analyzer.py
import ast
from models import ValidationResult

class CodeValidator:
    """Handles static analysis and syntax checking."""
    
    @staticmethod
    def validate_python_syntax(code: str) -> ValidationResult:
        """
        Attempts to parse the code into an AST. 
        If it fails, we know there is a syntax error.
        """
        errors = []
        warnings = []
        
        try:
            ast.parse(code)
            is_valid = True
        except SyntaxError as e:
            is_valid = False
            # Format a clean error message pointing to the exact line
            errors.append(f"Syntax Error on line {e.lineno}: {e.msg}\nCode: {e.text}")
        except Exception as e:
            is_valid = False
            errors.append(f"Unexpected parsing error: {str(e)}")
            
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)