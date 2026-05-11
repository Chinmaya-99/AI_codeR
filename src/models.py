# models.py
from pydantic import BaseModel, Field
from typing import Literal, List, Tuple, Optional
from dataclasses import dataclass

# --- LLM Output Models (Pydantic) ---
class CodeDiff(BaseModel):
    operation: Literal["replace", "insert", "delete"] = Field(
        description="The type of operation to perform."
    )
    start_line: int = Field(description="The starting line number (1-indexed).")
    end_line: int = Field(description="The ending line number (1-indexed). Inclusive.")
    new_code: str = Field(description="The new code snippet. Empty for delete.")
    reasoning: str = Field(description="One sentence explaining WHY this change is made.")

class DiffEngineOutput(BaseModel):
    diffs: List[CodeDiff] = Field(description="List of code modifications.")

# --- Internal Engine Models (Dataclasses) ---
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

@dataclass
class DiffApplicationResult:
    success: bool
    modified_code: str
    applied_diffs: List[CodeDiff]
    failed_diffs: List[Tuple[CodeDiff, str]]  # (diff object, error message)
    validation: ValidationResult