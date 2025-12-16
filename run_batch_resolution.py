import pandas as pd
import argparse
import sys
import os

# Ensure we can import from the local package
sys.path.append(os.getcwd())

from payee_resolution.logic import identify_real_payee

def main():
    parser = argparse.ArgumentParser(description="Resolve payees from a CSV file.")
    parser.add_argument("input_file", help="Path to input CSV file")
    parser.add_argument("--output", help="Path to output CSV file", default="resolved_payees.csv")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return

    try:
        df = pd.read_csv(args.input_file)
        
        # Determine which column contains the payees
        payee_col = None
        
        # 1. Check for '0' (common in the provided dataset)
        if "0" in df.columns:
            payee_col = "0"
        # 2. Check for explicit 'payee' column (case-insensitive)
        elif any(c.lower() == "payee" for c in df.columns):
            payee_col = next(c for c in df.columns if c.lower() == "payee")
        # 3. Fallback to the first column
        else:
            payee_col = df.columns[0]
            
        payees = df[payee_col].dropna().astype(str)
        
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    results = []
    print(f"{ 'ORIGINAL PAYEE':<50} | { 'RESOLVED NAME':<30} | { 'CONFIDENCE':<10}")
    print("-" * 96)

    for payee in payees:
        # call the logic function directly
        real_name, confidence = identify_real_payee(payee)
        
        results.append({
            "original_payee": payee,
            "real_name": real_name,
            "confidence": confidence
        })
        
        # Truncate for display
        disp_orig = (payee[:47] + '..') if len(payee) > 47 else payee
        disp_real = (real_name[:27] + '..') if len(real_name) > 27 else real_name
        print(f"{disp_orig:<50} | {disp_real:<30} | {confidence:.2f}")

    # Save to output
    out_df = pd.DataFrame(results)
    out_df.to_csv(args.output, index=False)
    print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main()
