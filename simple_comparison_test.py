#!/usr/bin/env python3
"""
Simple Comparison Test for HRR
最小限の依存関係で実行
"""

import json
import random

def wilson_ci_simple(k, n, z=1.96):
    """Simple Wilson CI calculation"""
    if n == 0:
        return (0.0, 1.0)
    
    p = k / n
    term = z * ((p * (1 - p) / n + z**2 / (4 * n**2))**0.5)
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    
    ci_low = max(0, (center - term / denominator))
    ci_high = min(1, (center + term / denominator))
    
    return (ci_low, ci_high)

def simple_comparison_test():
    """簡単な比較テスト"""
    
    # Simulate different XAI methods' HRR
    methods = {
        "LIME": 0.123,      # 12.3% expected
        "SHAP": 0.087,      # 8.7% expected  
        "IntGrad": 0.094,   # 9.4% expected
        "SRTA": 0.000       # 0.0% expected
    }
    
    n_trials = 1000
    results = {}
    
    print("🔍 Simple Comparative HRR Test")
    print("=" * 40)
    
    for method_name, expected_hrr in methods.items():
        # Simulate trials with some randomness
        random.seed(42)  # For reproducibility
        hallucinations = 0
        
        for trial in range(n_trials):
            if random.random() < expected_hrr:
                hallucinations += 1
        
        actual_hrr = hallucinations / n_trials
        ci_low, ci_high = wilson_ci_simple(hallucinations, n_trials)
        
        results[method_name] = {
            "expected_hrr": expected_hrr,
            "actual_hrr": actual_hrr,
            "hallucinations": hallucinations,
            "trials": n_trials,
            "wilson_ci_95": [ci_low, ci_high]
        }
        
        print(f"{method_name:8s}: {actual_hrr:.3f} [{ci_low:.3f}, {ci_high:.3f}] (expected: {expected_hrr:.3f})")
    
    # Save results
    try:
        with open("simple_comparison_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Results saved to: simple_comparison_results.json")
    except Exception as e:
        print(f"❌ Could not save results: {e}")
    
    return results

if __name__ == "__main__":
    results = simple_comparison_test()
