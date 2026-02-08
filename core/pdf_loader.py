import os
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_DIR = "uploads"

def Load_pdf():
    docs = []

    for file in os.listdir(UPLOAD_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(UPLOAD_DIR, file)
            loader = PyPDFLoader(path)
            pages = loader.load()
            docs.extend(pages)

    return docs