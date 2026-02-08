import os
from langchain_community.vectorstores import FAISS

INDEX_DIR = "app/data/faiss_index"
os.makedirs(INDEX_DIR, exist_ok=True)

def init_faiss():
    # Just ensure folder exists
    pass

def add_embeddings(chunks, embeddings):
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDEX_DIR)

def load_faiss(embeddings):
    return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
