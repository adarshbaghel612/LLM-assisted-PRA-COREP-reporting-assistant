def validate_ca1(data):
    errors = []

    cet1_block = data.get("CET1", {})
    reg_adj = cet1_block.get("regulatory_adjustments") or {}

    # If regulatory_adjustments is None, treat as empty dict
    if not isinstance(reg_adj, dict):
        errors.append("CET1 regulatory_adjustments must be an object.")
        reg_adj = {}

    # Now safe to iterate
    for key, value in reg_adj.items():
        if value is None:
            errors.append(f"Missing value for CET1 adjustment: {key}")

    # Continue with the rest of your validation...
    return {"valid": len(errors) == 0, "errors": errors}
