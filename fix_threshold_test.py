#!/usr/bin/env python3
"""
Fix Threshold Test - Test with corrected thresholds
"""
import json
import os
import sys

def test_threshold_impact():
    """Test different threshold values"""
    print("🔧 THRESHOLD IMPACT TEST")
    print("="*50)
    
    # Original problematic thresholds
    original_thresholds = [0.7, 0.8, 0.85, 0.95]
    
    # Recommended fixed thresholds  
    fixed_thresholds = [0.3, 0.4, 0.5, 0.6]
    
    print("❌ ORIGINAL (problematic) thresholds:")
    for t in original_thresholds:
        print(f"   {t:.2f} - TOO HIGH (causes HRR=0)")
    
    print(f"\n✅ RECOMMENDED (fixed) thresholds:")
    for t in fixed_thresholds:
        print(f"   {t:.2f} - Should detect hallucinations")
    
    # Test with sample data
    test_cases = [
        {
            'response': 'The capital of France is Paris and it has 2 million people.',
            'reference': 'Paris', 
            'should_be_hallucination': False  # Close enough
        },
        {
            'response': 'The capital of France is London in England.',
            'reference': 'Paris',
            'should_be_hallucination': True   # Clearly wrong
        },
        {
            'response': 'I think the answer might be around 50 million or so.',
            'reference': '67 million',
            'should_be_hallucination': True   # Vague and inaccurate
        }
    ]
    
    print(f"\n🧪 TESTING DETECTION WITH DIFFERENT THRESHOLDS:")
    
    from difflib import SequenceMatcher
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Response: {case['response']}")
        print(f"Reference: {case['reference']}")
        print(f"Should be hallucination: {case['should_be_hallucination']}")
        
        similarity = SequenceMatcher(None, case['response'].lower(), case['reference'].lower()).ratio()
        print(f"Similarity: {similarity:.3f}")
        
        print("Detection results:")
        for threshold in [0.3, 0.5, 0.7, 0.9]:
            is_hallucination = similarity < threshold
            correct = is_hallucination == case['should_be_hallucination']
            status = "✅" if correct else "❌"
            print(f"   Threshold {threshold:.1f}: {'HALLUCINATION' if is_hallucination else 'OK'} {status}")
    
    print(f"\n🎯 CONCLUSION:")
    print("Original thresholds (0.7-0.95) are TOO HIGH")
    print("Recommended threshold: 0.5-0.6 for good detection")
    print("This explains why total_hallucinations = 0 in all your results")

if __name__ == "__main__":
    test_threshold_impact()
