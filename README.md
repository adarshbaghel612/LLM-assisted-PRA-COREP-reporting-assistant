First run pip install -r requirements.txt
run FastAPI Backend file with uvicorn main:app --reload or python -m uvicorn main:app --reload
then run Streamlit file with streamlit run UI.py or python -m streamlit run UI.py


1. Overview

This project is a prototype of an LLM-powered assistant designed to help with PRA COREP regulatory reporting.
It demonstrates a working pipeline from:

Question → Retrieval → LLM Reasoning → Structured Output → COREP Template Extract + Validation

The system handles a narrow scope (Own Funds template), but showcases how AI can reduce manual interpretation effort for regulatory analysts.

2. Features

Upload PRA Rulebook / COREP Instruction PDFs

Automatic extraction & vector indexing

Retrieval-augmented generation (RAG)

Strict JSON output following COREP schema

Inline rule paragraph justifications

Validation engine for inconsistencies

Human-readable template output

Streamlit user interface

3. Architecture

Core Components

Document loader: PDF → clean text

Text splitter: RecursiveCharacterTextSplitter

Embeddings & Vector DB: FAISS

Retriever: hybrid or semantic search

LLM reasoning: schema-guided JSON generation

Validator: numeric + logical validations

Renderer: template output

UI: Streamlit front-end
