# Initial known payees dictionary for Phase 1 & 2
KNOWN_PAYEES = {
    "7-eleven": "7-Eleven",
    "peet": "Peet's Coffee",
    "starbucks": "Starbucks",
    "mcdonald": "McDonald's",
    "chevron": "Chevron",
    "76": "76 Gas Station",
    "shell": "Shell",
    "safeway": "Safeway",
    "amazon": "Amazon",
    "texaco": "Texaco",
    "costco": "Costco",
    "whole foods": "Whole Foods Market",
    "trader joe": "Trader Joe's",
}

# Common abbreviations to expand or normalize during cleaning
ABBREVIATIONS = {
    "COF": "COFFEE",
    "MKT": "MARKET",
    "MKTP": "MARKETPLACE",
    "SQ": "SQUARE",
    "CTR": "CENTER",
    "ST": "STREET",
    "CO": "COMPANY",
}

# US State codes for removal (to strip location info)
US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
}

# Simulated historical data for clustering (Phase 3)
# In a real app, this would come from the database or csv.
TRAINING_DATA = [
    "LAKE CITY SEATTLE WA",
    "LAKE CITY 2304",
    "LAKE CITY WAY STORE",
    "AMAZN Mktp US*MM3ABCD",
    "Amazon Marketplace AMZN.COM/BILL WA",
    "AMAZON MKT 12345",
    "UBER TRIP 29384",
    "UBER *TRIP HELP.UBER.COM",
    "UBER EATS 21390"
]
