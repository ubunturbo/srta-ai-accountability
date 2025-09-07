#!/usr/bin/env python3
"""
Extract explanation data from scaled_evaluation_results.csv
"""

import pandas as pd
import json

def extract_original_data():
    """Extract your original 200 samples"""
    
    # Load your original results
    df = pd.read_csv('./evaluation_results/scaled_evaluation_results.csv')
    print(f"Loaded {len(df)} samples from scaled_evaluation_results.csv")
    print(f"Columns: {list(df.columns)}")
    
    # Show first few rows to understand structure
    print("\nFirst 3 rows:")
    print(df.head(3).to_string())
    
    # Look for explanation text columns
    text_cols = [col for col in df.columns if any(word in col.lower() 
                 for word in ['explanation', 'text', 'content', 'response'])]
    print(f"\nPotential text columns: {text_cols}")
    
    # Convert to multi-agent format
    converted_samples = []
    for i, row in df.iterrows():
        # You'll need to adjust these column names based on your actual data
        converted_samples.append({
            'id': f'original_{i+1:03d}',
            'task_type': row.get('dataset', 'unknown'),  # Adjust column name
            'explanation_text': row.get('explanation_text', ''),  # Adjust column name  
            'original_srta_score': row.get('overall_score', None),  # Adjust column name
            'ground_truth': row.get('ground_truth', None)  # Adjust column name
        })
    
    # Save converted data
    converted_df = pd.DataFrame(converted_samples)
    converted_df.to_csv('data/original_200_samples.csv', index=False)
    
    print(f"\nConverted {len(converted_samples)} samples")
    print("Saved to data/original_200_samples.csv")
    
    return converted_df

def check_json_data():
    """Also check JSON results for additional context"""
    
    json_files = [
        './evaluation_results/scaled_evaluation_results.json',
        './evaluation_results/correlation_analysis_scaled.json'
    ]
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            print(f"\n{json_file} structure:")
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
            elif isinstance(data, list):
                print(f"List with {len(data)} items")
                if data:
                    print(f"First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

if __name__ == "__main__":
    print("=== Extracting Original Research Data ===")
    extract_original_data()
    check_json_data()
