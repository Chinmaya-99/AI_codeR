# Diff_engine.py

class DiffEngine:
    """
    Applies structured code edits to an original string of code.
    Safely handles line shifting by applying patches from bottom to top.
    """
    
    def __init__(self):
        pass

    def apply_edits(self, original_code: str, edits: list) -> str:
        """
        Takes the original code and the list of CodeDiff Pydantic objects.
        Returns the final modified code string.
        """
        # 1. Split the original code into a list of lines
        # (Assuming the LLM uses 1-based indexing for line numbers)
        lines = original_code.split('\n')
        
        # 2. Sort edits in REVERSE order by start_line
        # This prevents index shifting for subsequent operations!
        sorted_edits = sorted(edits, key=lambda x: x.start_line, reverse=True)
        
        for edit in sorted_edits:
            # Convert 1-based LLM line numbers to 0-based Python list indices
            start_idx = edit.start_line - 1
            
            # For inserts, end_line might be the same as start_line, 
            # but for replace/delete, we need the exact block.
            end_idx = edit.end_line - 1
            
            # Split the LLM's new code string into a list of lines
            new_lines = edit.new_code.strip().split('\n') if edit.new_code else []
            
            if edit.operation == 'replace':
                # Slice out the old lines and inject the new ones
                lines[start_idx:end_idx + 1] = new_lines
                
            elif edit.operation == 'delete':
                # Delete the specific block of lines
                del lines[start_idx:end_idx + 1]
                
            elif edit.operation == 'insert':
                # Insert the new code exactly at the start_idx
                # (Pushes the current start_idx line downwards)
                lines[start_idx:start_idx] = new_lines
                
        # 3. Join it all back together
        return '\n'.join(lines)

# --- Quick Test Block (You can remove this in production) ---
if __name__ == "__main__":
    # Mocking your Llm.py output to test the engine
    class MockDiff:
        def __init__(self, op, start, end, code):
            self.operation = op
            self.start_line = start
            self.end_line = end
            self.new_code = code

    sample_code = "def hello():\n    print('Hello')\n    print('World')\n    return False"
    
    # Let's say the LLM wants to replace 'World' with 'CACE' and change return to True
    mock_edits = [
        MockDiff("replace", 3, 3, "    print('CACE')"),
        MockDiff("replace", 4, 4, "    return True")
    ]
    
    engine = DiffEngine()
    updated_code = engine.apply_edits(sample_code, mock_edits)
    
    print("--- Original ---")
    print(sample_code)
    print("\n--- Updated ---")
    print(updated_code)