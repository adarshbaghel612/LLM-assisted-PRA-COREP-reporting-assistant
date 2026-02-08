def validate_ca1(data):
    errors = []
    warnings = []

    CET1 = data["CET1"]["CET1_total"]
    AT1 = data["AT1"]["AT1_total"]
    Tier2 = data["Tier2"]["Tier2_total"]
    Tier1_total = data["Totals"]["Tier1_total"]
    own_funds_total = data["Totals"]["own_funds_total"]

    if CET1 is not None and AT1 is not None:
        expected_tier1 = CET1 + AT1
        if Tier1_total != expected_tier1:
            errors.append(f"Tier1_total ({Tier1_total}) ≠ CET1_total ({CET1}) + AT1_total ({AT1})")

    # Validate Own Funds = Tier1 + Tier2
    if Tier1_total is not None and Tier2 is not None:
        expected_own_funds = Tier1_total + Tier2
        if own_funds_total != expected_own_funds:
            errors.append(f"own_funds_total ({own_funds_total}) ≠ Tier1_total ({Tier1_total}) + Tier2_total ({Tier2})")

    # ---------------------------
    # REGULATORY ADJUSTMENTS CHECK
    # ---------------------------
    for key, value in data["CET1"]["regulatory_adjustments"].items():
        if value is None:
            continue
        if value > 0:
            warnings.append(f"Regulatory adjustment '{key}' must be negative (found {value}).")

    return {
        "errors": errors,
        "warnings": warnings
    }

