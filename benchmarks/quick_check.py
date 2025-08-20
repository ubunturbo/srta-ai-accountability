"""
SRTA Quick Check - Minimal Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🚀 SRTA Quick Check")

try:
    from src.srta.evaluation.evaluation_layer import EvaluationLayer
    
    evaluator = EvaluationLayer()
    result = evaluator.evaluate_explanation({
        'explanation_text': 'This is a simple test explanation.'
    })
    
    print(f"✅ Overall Quality: {result.metrics.overall:.1%}")
    print(f"✅ Quality Level: {result.quality_level.value}")
    print("🎊 Quick check successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")

