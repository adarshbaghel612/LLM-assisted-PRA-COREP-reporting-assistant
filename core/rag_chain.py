from langchain_google_genai import ChatGoogleGenerativeAI
from core.embeddings import get_embeddings
from core.vector_store import load_faiss
from dotenv import load_dotenv
import os
from models.ca1_prompt import CA1_PROMPT

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GEMINI_API_KEY)

def generate_answer(query):
    embeddings = get_embeddings()
    db = load_faiss(embeddings)
    retriever = db.as_retriever()

    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = CA1_PROMPT

    response = llm.invoke(prompt)
    return response.content
