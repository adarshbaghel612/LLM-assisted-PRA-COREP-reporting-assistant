from fastapi import FastAPI,APIRouter
from models.input import QueryRequest 
from datetime import datetime
from api.llm import generate_structured_output
from validator.CA1 import validate_ca1
from Render.render_ca1 import render_ca1_extract
from api.llm import llm
from Intent.intent import classify_intent


app=FastAPI()
router=APIRouter(prefix="/chat",tags=["Chat"])

@router.post("/chat")
async def chat(prompt:QueryRequest):

    intent = classify_intent(prompt.question, llm)
    response=generate_structured_output(prompt.question,prompt.scenario)
    validation=validate_ca1(response)
    extract=render_ca1_extract(response)
    
    audit = {
        "references": response.get("references", {}),
        "timestamp": datetime.utcnow().isoformat()
    }
    intent = intent.strip().lower()
    

    if intent in ["extract","CA1 COREP","ca1 corep","template extract","corep extract"]:
        return {"template_extract": extract}

    if intent in ["structured","Structured CA1 JSON","json", "ca1 json"]:
        return {"structured_output": response}

    if intent in ["validation","validated", "check", "consistency check"]:
        return {"validation": validation}

    if intent in ["references","source","citations","rules used"]:
        return {"references": audit["references"]}

    return {
        "validation": validation,
        "structured_output": response,
        "template_extract": extract,
        "audit_log": audit
    }

app.include_router(router)