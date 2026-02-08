from Intent.intent_prompt import INTENT_PROMPT
from api.llm import llm

def classify_intent(question: str, llm):
    prompt = INTENT_PROMPT.replace("{question}", question)
    response = llm.invoke(prompt)

    intent = response.content.strip().lower()

    valid_intents = ["extract", "CA1 COREP","ca1 corep","template extract","corep extract",
                     "structured", "Structured CA1 JSON","json", "ca1 json",
                     "validated", "check", "consistency check",
                     "validation","source","citations","rules used",
                     "references", "full"]

    if intent not in valid_intents:
        return "full"

    return intent
