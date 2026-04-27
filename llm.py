from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_openrouter import ChatOpenRouter

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal,List


#creating parser output:


class CodeDiff(BaseModel):
    operation: Literal["replace", "insert", "delete"] = Field(alias="OPERATION")
    start_line: int = Field(alias="START_LINE")
    end_line: int = Field(alias="END_LINE")
    new_code: str = Field(alias="NEW_CODE")
    reasoning: str = Field(alias="REASONING")
class DiffEngineOutput(BaseModel):
    edits: List[CodeDiff] 
parser = PydanticOutputParser(pydantic_object=DiffEngineOutput)

#______________________________________________

#loading model and initiaing it
load_dotenv()

gemini=ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite-preview',temperature=0.0).with_structured_output(DiffEngineOutput)
gemma=ChatOpenRouter(model='google/gemma-4-31b-it:free',temperature=0.7).with_structured_output(DiffEngineOutput)

# 2. Create a Fallback Chain
# If gemini hits a rate limit or traffic error, it automatically triggers gemma
chain_with_fallback = gemini.with_fallbacks([gemma])
#_______________________________________________________________________________________

#________________________________________________________________
#prompt 

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a code diff generator. You MUST respond in this exact format:
Rules:
- Only fix syntax or logical errors
- Do NOT rewrite full code
- Return ONLY minimal diff

{format_instructions}
      
Only return valid structured output.
NEVER output full files. ONLY the minimal change with two time verification to give optimal result."""),
    ("human", "Fix this code:\n{code}")
])

prompt_with_instructions = prompt.partial(format_instructions=parser.get_format_instructions())
new_prompt=prompt_with_instructions
#___________________________________________________________________________
final_chain = new_prompt | chain_with_fallback

# 3. Execution & Error Handling
# ---------------------------------------------------------
if __name__ == "__main__":
    target_code = input("Give your code:\n")
    
    try:
        # Invoke the chain
        result = final_chain.invoke({"code": target_code})
        
        print("\n--- Parsed Edits ---\n")
        # Iterate through the list of edits
        for i, edit in enumerate(result.edits, 1):
            print(f"Edit #{i}: [{edit.operation.upper()}] Lines {edit.start_line}-{edit.end_line}")
            print(f"Reasoning: {edit.reasoning}")
            print(f"New Code:\n{edit.new_code}\n{'-'*20}")
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")
