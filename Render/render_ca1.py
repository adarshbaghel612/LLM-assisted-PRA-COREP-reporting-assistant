def render_ca1_extract(structured: dict):
    cet1 = structured["CET1"]["CET1_total"]
    at1 = structured["AT1"]["AT1_total"]
    tier2 = structured["Tier2"]["Tier2_total"]
    tier1 = structured["Totals"]["Tier1_total"]
    total_own_funds = structured["Totals"]["own_funds_total"]

    
    extract = [
        {
            "row": "010",
            "desc": "CET1 Capital",
            "value": cet1
        },
        {
            "row": "050",
            "desc": "AT1 Capital",
            "value": at1
        },
        {
            "row": "090",
            "desc": "Tier 1 Capital",
            "value": tier1
        },
        {
            "row": "100",
            "desc": "Tier 2 Capital",
            "value": tier2
        },
        {
            "row": "150",
            "desc": "Total Own Funds",
            "value": total_own_funds
        }
    ]

    return extract
