import os
import json
from models.ca1_prompt import CA1_PROMPT
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from core.embeddings import get_embeddings
from core.vector_store import load_faiss

load_dotenv()
parser = JsonOutputParser()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY)

def generate_structured_output(question: str,scenario: str):
    embeddings = get_embeddings()
    db = load_faiss(embeddings)
    retriever = db.as_retriever()
    docs = retriever.invoke(question)
    doc_context = "\n\n".join([d.page_content for d in docs])
    final_prompt = CA1_PROMPT.replace("{scenario}", scenario).replace("{context}", doc_context)

    response = llm.invoke(final_prompt)

    raw_output = response.content

    # --- CLEAN JSON FENCES ---
    clean_output = raw_output.strip()

    if clean_output.startswith("```"):
        clean_output = clean_output.replace("```json", "")
        clean_output = clean_output.replace("```", "")
        clean_output = clean_output.strip()

    # --- PARSE JSON ---
    try:
        return json.loads(clean_output)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by LLM after cleaning",
            "raw_output": clean_output
        }