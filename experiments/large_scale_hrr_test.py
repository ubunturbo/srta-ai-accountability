#!/usr/bin/env python3
"""
Large Scale HRR Test
n=2,000 → n=10,000 への拡張
"""

import json
import argparse
from experiments.hallucination_reproduction import run_experiment, wilson_ci

def extended_scale_validation(max_trials: int = 10000):
    """
    n=2,000 → n=10,000 への拡張
    統計的信頼度の強化
    """
    
    # 段階的拡張
    sample_sizes = [2000, 5000, 10000]
    
    results = {}
    
    for n in sample_sizes:
        print(f"\n🔍 Testing with n={n} trials...")
        
        # Using existing HRR experiment framework
        result = run_experiment(
            model="gpt-4o-mini",
            dataset_name="truthfulqa",
            n_items=100,
            n_trials_per_item=n // 100,  # Distribute trials across items
            temperatures=[0.7],  # Use standard temperature
            seed_base=42
        )
        
        # Calculate overall statistics
        total_hallucinations = sum(item.get("total_hallucinations", 0) for item in result)
        total_trials = sum(item.get("n_trials", 0) for item in result)
        
        overall_hrr = total_hallucinations / total_trials if total_trials > 0 else 0.0
        ci_low, ci_high = wilson_ci(total_hallucinations, total_trials)
        
        results[f"n_{n}"] = {
            "sample_size": n,
            "total_trials": total_trials,
            "total_hallucinations": total_hallucinations,
            "hallucination_rate": overall_hrr,
            "wilson_ci_95": [ci_low, ci_high]
        }
        
        print(f"  Results: {overall_hrr:.4f} [{ci_low:.4f}, {ci_high:.4f}]")
    
    # Save consolidated results
    with open("results_large_scale_hrr.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Validate CI convergence
    validate_ci_convergence(results)
    
    return results

def validate_ci_convergence(results: dict):
    """Wilson CI収束の確認"""
    print("\n📈 CI Convergence Analysis:")
    
    for key, data in results.items():
        n = data["sample_size"]
        ci_width = data["wilson_ci_95"][1] - data["wilson_ci_95"][0]
        print(f"  n={n:5d}: CI width = {ci_width:.6f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-trials", type=int, default=10000)
    args = parser.parse_args()
    
    print("📊 Large Scale HRR Validation")
    print("=" * 40)
    
    results = extended_scale_validation(args.max_trials)
    
    print("\n✅ Large scale validation completed")
    print("📁 Results saved to: results_large_scale_hrr.json")
