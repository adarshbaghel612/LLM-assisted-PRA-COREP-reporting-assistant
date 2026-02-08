import streamlit as st
import json
import requests

st.set_page_config(page_title="CA1 COREP Reporting Assistant", layout="wide")

st.title("📘 CA1 COREP Reporting Assistant")
st.write("LLM-assisted PRA COREP CA1 Reporting")

# ---------------------------------------
# Input Section
# ---------------------------------------
st.header("📥 Input")

question = st.text_input(
    "Enter your question",
    value="Render the CA1 COREP extract for this scenario."
)

scenario = st.text_area(
    "Enter scenario",
    value="Common equity £600m; Share premium £200m; OCI £50m; PVA deduction £10m; Goodwill deduction £30m; AT1 £150m; Tier2 £180m",
    height=130
)

if st.button("Submit"):
    st.write("")

    with st.spinner("Processing…"):
        response = requests.post(
            "http://localhost:8000/chat/chat",      # your backend endpoint
            json={"question": question, "scenario": scenario}
        )

    if response.status_code != 200:
        st.error(f"❌ API Error: {response.text}")
        st.stop()

    results = response.json()

    st.success("Response received!")

    # ---------------------------------------
    # INTENT SWITCH — auto detect response type
    # ---------------------------------------

    # CASE 1: Only extract was returned
    if "template_extract" in results and len(results.keys()) == 1:
        st.header("📄 CA1 COREP Extract")
        st.table(results["template_extract"])
        st.stop()

    # CASE 2: Only structured_output returned
    if "structured_output" in results and len(results.keys()) == 1:
        st.header("🧱 Structured CA1 JSON Output")
        st.json(results["structured_output"])
        st.stop()

    # CASE 3: Only validation returned
    if "validation" in results and len(results.keys()) == 1:
        st.header("🔍 Validation Results")
        st.json(results["validation"])
        st.stop()

    # CASE 4: Only references returned
    if "references" in results and len(results.keys()) == 1:
        st.header("📚 References (Audit Log)")
        st.json(results["references"])
        st.stop()

    # ---------------------------------------
    # DEFAULT CASE → Full CA1 Output
    # ---------------------------------------

    # VALIDATION
    st.header("🔍 Validation Summary")
    val = results.get("validation", {})
    if val.get("errors"):
        st.error("Errors found:")
        st.json(val["errors"])
    else:
        st.success("No validation errors")

    if val.get("warnings"):
        st.warning("Warnings:")
        st.json(val["warnings"])
    else:
        st.info("No warnings")

    # CA1 Extract Table
    st.header("📄 CA1 COREP Extract")
    st.table(results.get("template_extract", []))

    # Structured Output JSON
    st.header("🧱 Structured Output (CA1 Schema)")
    st.json(results.get("structured_output", {}))

    # References
    st.header("📚 References (Audit Log)")
    st.json(results["structured_output"].get("references", {}))

    # Missing fields
    st.header("⚠ Missing Fields")
    missing = results["structured_output"].get("missing_fields", {})
    if missing:
        for k, v in missing.items():
            st.warning(f"**{k}** → {v}")
    else:
        st.info("No missing fields.")
