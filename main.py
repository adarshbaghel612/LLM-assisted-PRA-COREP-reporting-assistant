from fastapi import FastAPI
from api import ingest, chat,health
app = FastAPI()

app.include_router(ingest.router)
app.include_router(chat.router)
app.include_router(health.router)





