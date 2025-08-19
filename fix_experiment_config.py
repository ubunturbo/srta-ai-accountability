#!/usr/bin/env python3
"""
Fix Experiment Configuration - Lower thresholds to enable detection
"""
import re

def fix_semantic_thresholds():
    """Fix the semantic thresholds in experiment_runner.py"""
    print("🔧 FIXING SEMANTIC THRESHOLDS")
    print("="*50)
    
    # Read original file
    with open('experiments/experiment_runner.py', 'r') as f:
        content = f.read()
    
    # Find and replace problematic thresholds
    replacements = {
        'semantic_threshold=0.7': 'semantic_threshold=0.5',
        'semantic_threshold=0.8': 'semantic_threshold=0.6', 
        'semantic_threshold=0.85': 'semantic_threshold=0.6',
        'semantic_threshold=0.95': 'semantic_threshold=0.7'
    }
    
    fixed_content = content
    changes_made = []
    
    for old, new in replacements.items():
        if old in fixed_content:
            fixed_content = fixed_content.replace(old, new)
            changes_made.append(f"{old} → {new}")
    
    if changes_made:
        # Write fixed version
        with open('experiments/experiment_runner_fixed.py', 'w') as f:
            f.write(fixed_content)
        
        print("✅ Changes made:")
        for change in changes_made:
            print(f"   {change}")
        
        print(f"\n📁 Fixed file saved as: experiments/experiment_runner_fixed.py")
        print("🔧 To apply: mv experiments/experiment_runner_fixed.py experiments/experiment_runner.py")
        
    else:
        print("⚠️ No semantic_threshold patterns found to fix")
    
    return len(changes_made) > 0

if __name__ == "__main__":
    fix_semantic_thresholds()
