import re
import difflib
from typing import Tuple, Optional
from .data import KNOWN_PAYEES, ABBREVIATIONS, US_STATES, TRAINING_DATA
from .clustering import PayeeClusterer

# Initialize Clusterer Global (simulating startup load)
# We train it once on import for this demo.
_clusterer = PayeeClusterer(n_clusters=3) # We have Lake City, Amazon, Uber groups
_clusterer.fit(TRAINING_DATA)

def clean_payee_string(payee: str) -> str:
    """
    Cleans the raw payee string by removing digits, location codes, 
    expanding abbreviations, and normalizing whitespace.
    """
    # Uppercase for consistent processing
    cleaned = payee.upper()
    
    # 1. Remove standalone digits (address numbers, zip codes)
    cleaned = re.sub(r'\b\d+\b', ' ', cleaned)
    
    # 2. Remove special chars but PRESERVE hyphens (for 7-Eleven) and spaces
    cleaned = re.sub(r'[^A-Z\s\-]', ' ', cleaned)
    
    # Tokenize
    tokens = cleaned.split()
    
    processed_tokens = []
    for token in tokens:
        # 3. Remove State Codes
        if token in US_STATES:
            continue
            
        # 4. Remove Country Codes
        if token in ["US", "SG", "UK", "CA"]: 
            continue
            
        # 5. Expand Abbreviations
        if token in ABBREVIATIONS:
            processed_tokens.append(ABBREVIATIONS[token])
        else:
            processed_tokens.append(token)
            
    # Reassemble
    cleaned = " ".join(processed_tokens)
    
    # 6. Final whitespace normalization
    cleaned = cleaned.strip()
    
    return cleaned

def match_known_payee(cleaned_payee: str) -> Tuple[Optional[str], float]:
    """
    Checks for exact substring matches in the known payee dictionary.
    Returns (real_name, confidence) if found, else (None, 0.0).
    """
    lower_input = cleaned_payee.lower()
    
    for key, real_name in KNOWN_PAYEES.items():
        if key in lower_input:
            return real_name, 0.95
            
    return None, 0.0

def fuzzy_match_payee(cleaned_payee: str) -> Tuple[Optional[str], float]:
    """
    Uses fuzzy matching to find a similar known payee key.
    Checks both the full cleaned string and individual tokens.
    Returns (real_name, confidence) if a good match is found.
    """
    target = cleaned_payee.lower()
    if not target:
        return None, 0.0
    
    best_ratio = 0.0
    best_name = None
    
    # 1. Compare tokens against keys (handles "Starbuks 123 Main St")
    tokens = target.split()
    
    for key, real_name in KNOWN_PAYEES.items():
        # Strategy A: Compare key against whole string
        ratio_full = difflib.SequenceMatcher(None, target, key).ratio()
        
        # Strategy B: Compare key against each token
        ratio_token = 0.0
        if tokens:
            ratio_token = max(difflib.SequenceMatcher(None, t, key).ratio() for t in tokens)
            
        current_max = max(ratio_full, ratio_token)
        
        if current_max > best_ratio:
            best_ratio = current_max
            best_name = real_name

    if best_ratio >= 0.8:
        return best_name, best_ratio
        
    return None, 0.0

def cluster_predict_payee(payee: str) -> Tuple[Optional[str], float]:
    """
    Uses the trained ML clusterer to predict the payee name.
    """
    try:
        predicted_name = _clusterer.predict(payee)
        if predicted_name and predicted_name != "Unknown":
            # Confidence is high because it's based on group similarity
            return predicted_name, 0.85
    except Exception:
        # Fallback if clustering fails or not fitted
        pass
    return None, 0.0

def identify_real_payee(payee: str) -> Tuple[str, float]:
    """
    Identifies the real payee name using a pipeline of:
    1. Cleaning
    2. Exact/Substring Dictionary Match
    3. Fuzzy Match
    4. ML Clustering (New in Phase 3)
    5. Fallback
    """
    # 1. Clean
    cleaned_payee = clean_payee_string(payee)
    
    # 2. Exact Match (Best source)
    real_name, confidence = match_known_payee(cleaned_payee)
    if real_name:
        return real_name, confidence
        
    # 3. Fuzzy Match (Second best)
    real_name, confidence = fuzzy_match_payee(cleaned_payee)
    if real_name:
        return real_name, confidence

    # 4. ML Clustering (New)
    # If standard rules failed, try the ML model on the ORIGINAL string
    # (The model was trained on raw strings, or at least similar raw strings)
    ml_name, ml_conf = cluster_predict_payee(payee)
    if ml_name:
        return ml_name, ml_conf
        
    # 5. Fallback
    if not cleaned_payee:
        return payee, 0.0 
        
    return cleaned_payee.title(), 0.4