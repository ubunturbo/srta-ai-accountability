#!/usr/bin/env python3
import json

def analyze_all_results():
    """全ベンチマーク結果の分析"""
    
    print("🎯 SRTA Benchmark Results Summary")
    print("=" * 50)
    
    # 既存のHRR結果
    try:
        with open("results_hrr_n2000_summary.json") as f:
            original = json.load(f)
        print("📊 Original HRR Test (n=2,000):")
        for temp, data in original.items():
            ci = data["wilson_ci_95"]
            print(f"  T={temp}: {data['per_trial_rate']:.1%} [{ci[0]:.1%}, {ci[1]:.1%}]")
    except:
        print("❌ Original results not found")
    
    # 比較結果
    try:
        with open("results_comparative_hrr.json") as f:
            comparative = json.load(f)
        print("\n🔄 Comparative Analysis:")
        for method, data in comparative.items():
            hrr = data["hallucination_rate"]
            ci = data["wilson_ci_95"]
            print(f"  {method:8s}: {hrr:.1%} [{ci[0]:.1%}, {ci[1]:.1%}]")
    except:
        print("❌ Comparative results not found")
    
    # スケールアップ結果
    try:
        with open("results_large_scale_hrr.json") as f:
            large_scale = json.load(f)
        print("\n📈 Scale Validation:")
        for key, data in large_scale.items():
            n = data["sample_size"]
            hrr = data["hallucination_rate"]
            ci = data["wilson_ci_95"]
            print(f"  n={n:5d}: {hrr:.1%} [{ci[0]:.1%}, {ci[1]:.1%}]")
    except:
        print("❌ Large scale results not found")

if __name__ == "__main__":
    analyze_all_results()
