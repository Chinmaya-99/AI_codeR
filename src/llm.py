from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from models import DiffEngineOutput
from analyzer import CodeValidator, ValidationResult

# loading model and initiaing it
load_dotenv()

validator = CodeValidator()


class llminit:
    def __init__(self):
        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite-preview", temperature=0.0
        ).with_structured_output(DiffEngineOutput)
        self.lamma = ChatGroq(
            model="llama-3.1-8b-instant", temperature=0.0
        ).with_structured_output(DiffEngineOutput)

        self.chain_with_fallback = self.gemini.with_fallbacks([self.lamma])
        # _______________________________________________________________________________________

        # prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a code diff generator. You MUST respond in this exact format:
                CRITICAL INSTRUCTIONS:
                - Only fix syntax or logical errors
                - Do NOT rewrite full code
                - Return ONLY minimal diff
                - Each diff must modify ONLY the specified lines
                - Do NOT merge multiple lines into one
                - Preserve line breaks exactly
                - Use 'replace' to change existing lines AND to fix missing syntax (like colons, commas, or parentheses)
                - NEVER use 'insert' to fix an existing line. 
                - Use 'insert' ONLY if you are writing a completely new, multi-line block of code from scratch
                - Each diff must specify exact line numbers from the formatted code
                Only return valid structured output.
                NEVER output full files. ONLY the minimal change with two time verification to give optimal result.""",
                ),
                (
                    "human",
                    "Intent: {intent}\n\nTarget Code:\n{code}\n\nANALYSIS RESULT:{analysis}",
                ),
            ]
        )
        self.final_chain = self.prompt | self.chain_with_fallback

    # 3. Execution
    def get_edits(self, intent: str, target_code: str, formatted_errors: str) -> DiffEngineOutput:
        """Invokes the LLM and returns structured diffs."""
        
        return self.final_chain.invoke(
            {"intent": intent, "code": target_code, "analysis": formatted_errors}
        )
    