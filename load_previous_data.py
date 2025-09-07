#!/usr/bin/env python3
"""
Load your previous 200-sample dataset for multi-agent comparison
"""

import pandas as pd
import os
from multi_agent_srta import MultiAgentSRTA, ExplanationSample

def create_sample_dataset():
    """Create a template showing the expected format"""
    
    # This is the format we need your data in:
    template_data = []
    
    for i in range(200):
        template_data.append({
            'id': f'previous_{i+1:03d}',
            'task_type': 'CoLA' if i % 2 == 0 else 'XNLI', 
            'explanation_text': f'Your actual explanation text from sample {i+1}',
            'original_srta_score': None,  # Your original single-agent scores if available
            'ground_truth': None  # Task ground truth if available
        })
    
    df = pd.DataFrame(template_data)
    df.to_csv('data/template_200_samples.csv', index=False)
    print("Created template at data/template_200_samples.csv")
    print("Replace with your actual data and run process_200_samples.py")

def process_200_samples(csv_path: str):
    """Process your 200 samples through multi-agent system"""
    
    if not os.path.exists(csv_path):
        print(f"Data file {csv_path} not found.")
        print("Run with --create-template first")
        return
    
    # Load data
    df = pd.read_csv(csv_path)
    print(f"Loading {len(df)} samples from {csv_path}")
    
    # Convert to ExplanationSample objects
    samples = []
    for _, row in df.iterrows():
        sample = ExplanationSample(
            id=row['id'],
            task_type=row['task_type'],
            explanation_text=row['explanation_text'],
            ground_truth=row.get('ground_truth')
        )
        samples.append(sample)
    
    # Initialize multi-agent system
    print("Initializing multi-agent evaluation system...")
    multi_agent = MultiAgentSRTA()
    
    if not multi_agent.load_models():
        print("Warning: Model loading issues, using fallback evaluation")
    
    # Process all samples
    print(f"Processing {len(samples)} samples...")
    
    results = []
    for i, sample in enumerate(samples):
        if i % 10 == 0:
            print(f"Progress: {i}/{len(samples)} samples processed")
        
        try:
            result = multi_agent.evaluate_explanation(sample)
            results.append(result)
        except Exception as e:
            print(f"Error processing {sample.id}: {e}")
            continue
    
    # Save results
    output_path = 'outputs/full_200_sample_results.csv'
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_path, index=False)
    
    print(f"\nCompleted! {len(results)} samples processed")
    print(f"Results saved to {output_path}")
    
    # Quick analysis
    if len(results) > 0:
        consensus_scores = [r['consensus_overall'] for r in results]
        print(f"Score range: {min(consensus_scores):.2f} - {max(consensus_scores):.2f}")
        print(f"Average: {sum(consensus_scores)/len(consensus_scores):.2f}")
        print(f"Variance: {pd.Series(consensus_scores).var():.4f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-template", action="store_true", 
                       help="Create template CSV file")
    parser.add_argument("--input", default="data/your_200_samples.csv",
                       help="Input CSV file with your data")
    
    args = parser.parse_args()
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    if args.create_template:
        create_sample_dataset()
    else:
        process_200_samples(args.input)
