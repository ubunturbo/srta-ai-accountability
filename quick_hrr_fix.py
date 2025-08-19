#!/usr/bin/env python3
"""
Quick HRR Fix Script for SRTA
=============================
Analyzes existing results and fixes HRR=0 problem
"""

import os
import json
import glob
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np

def analyze_jsonl_file(file_path):
    """Analyze a JSONL results file"""
    print(f"\n📊 Analyzing: {file_path}")
    
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data.append(json.loads(line.strip()))
                except json.JSONDecodeError as e:
                    if line_num <= 5:  # Only report first few errors
                        print(f"   Line {line_num} JSON error: {e}")
        
        print(f"✅ Loaded {len(data)} records from {file_path}")
        
        if not data:
            return None
            
        # Analyze structure
        sample = data[0]
        print(f"🔍 Sample structure: {list(sample.keys())}")
        
        # Look for hallucination detection
        hallucination_count = 0
        total_count = len(data)
        
        # Check different possible field names
        halluc_field = None
        for field_name in ['is_hallucination', 'hallucination_detected', 'has_hallucination', 'hallucinates']:
            if field_name in sample:
                halluc_field = field_name
                break
        
        if halluc_field:
            hallucination_count = sum(1 for item in data if item.get(halluc_field, False))
            print(f"📈 Hallucination field '{halluc_field}': {hallucination_count}/{total_count} ({hallucination_count/total_count:.1%})")
        else:
            print("⚠️  No clear hallucination field found in:", list(sample.keys()))
        
        # Calculate conditional HRR if possible
        if 'item_id' in sample or 'question_id' in sample:
            id_field = 'item_id' if 'item_id' in sample else 'question_id'
            items = defaultdict(list)
            
            for record in data:
                item_id = record.get(id_field)
                items[item_id].append(record)
            
            items_with_hallucinations = 0
            conditional_scores = []
            
            for item_id, records in items.items():
                if halluc_field:
                    hallucinations = [r.get(halluc_field, False) for r in records]
                    if any(hallucinations):
                        items_with_hallucinations += 1
                        # Pattern consistency (simplified)
                        pattern_rate = sum(hallucinations) / len(hallucinations)
                        conditional_scores.append(pattern_rate)
            
            conditional_hrr = np.mean(conditional_scores) if conditional_scores else 0.0
            
            print(f"🎯 Conditional HRR Analysis:")
            print(f"   - Total unique items: {len(items)}")
            print(f"   - Items with hallucinations: {items_with_hallucinations}")
            print(f"   - Coverage: {items_with_hallucinations/len(items):.1%}")
            print(f"   - Conditional HRR: {conditional_hrr:.3f}")
            
            return {
                'file': file_path,
                'total_records': total_count,
                'total_items': len(items),
                'items_with_hallucinations': items_with_hallucinations,
                'conditional_hrr': conditional_hrr,
                'hallucination_rate': hallucination_count/total_count if total_count > 0 else 0
            }
        
        return {
            'file': file_path,
            'total_records': total_count,
            'hallucination_rate': hallucination_count/total_count if total_count > 0 else 0
        }
        
    except Exception as e:
        print(f"❌ Error analyzing {file_path}: {e}")
        return None

def main():
    print("🔧 SRTA HRR Quick Fix - Analyzing Existing Results")
    print("=" * 60)
    
    # Find and analyze all result files
    result_files = [
        'results_hrr_tscan.jsonl',  # Latest/largest
        'results_hrr_n2000.jsonl', 
        'results_hrr.jsonl'
    ]
    
    best_analysis = None
    
    for file_path in result_files:
        if os.path.exists(file_path):
            analysis = analyze_jsonl_file(file_path)
            if analysis and (not best_analysis or analysis.get('total_records', 0) > best_analysis.get('total_records', 0)):
                best_analysis = analysis
    
    if best_analysis:
        print(f"\n" + "="*60)
        print(f"🏆 BEST RESULTS ANALYSIS")
        print(f"File: {best_analysis['file']}")
        print(f"Total records: {best_analysis['total_records']:,}")
        
        if 'conditional_hrr' in best_analysis:
            print(f"Items with hallucinations: {best_analysis['items_with_hallucinations']}")
            print(f"Conditional HRR: {best_analysis['conditional_hrr']:.3f}")
            print(f"Coverage: {best_analysis['items_with_hallucinations']/best_analysis['total_items']:.1%}")
        
        print(f"Hallucination rate: {best_analysis['hallucination_rate']:.1%}")
        
        # Provide recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        if best_analysis['hallucination_rate'] == 0:
            print("🚨 CRITICAL: Zero hallucination rate detected!")
            print("1. Detection system is not working")
            print("2. Check similarity threshold (lower from 0.6 to 0.3)")
            print("3. Manually inspect answers vs references")
        elif best_analysis['hallucination_rate'] < 0.05:
            print("⚠️  Very low hallucination rate - detection may be too strict")
            print("1. Consider lowering detection threshold")
            print("2. Add LLM judge for borderline cases")
        elif 'conditional_hrr' in best_analysis:
            if best_analysis['conditional_hrr'] > 0.3:
                print("✅ Good conditional HRR - patterns are reproducing!")
                print(f"1. Use {best_analysis['conditional_hrr']:.3f} as primary HRR metric")
                print("2. Focus on temporal context variations for SRTA-TA")
            else:
                print("📈 Low conditional HRR - improve pattern detection")
                print("1. Analyze why patterns aren't reproducing consistently")
                print("2. Consider more runs per item")
        
        # Check if CSV summaries exist
        if os.path.exists('hrr_summary.csv'):
            print(f"\n📊 Additional analysis in: hrr_summary.csv")
        if os.path.exists('hrr_by_item.csv'):
            print(f"📊 Item-level analysis in: hrr_by_item.csv")
    
    else:
        print("❌ No valid result files found or analyzed")

if __name__ == "__main__":
    main()
