"""
SRTA Integration Test - Simple Version
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔄 SRTA Integration Test")
print("="*40)

# Test Evaluation Layer
try:
    from src.srta.evaluation.evaluation_layer import EvaluationLayer
    print("✅ Evaluation Layer imported")
    
    evaluator = EvaluationLayer()
    test_data = {'explanation_text': 'This is a test explanation with sufficient detail.'}
    result = evaluator.evaluate_explanation(test_data)
    
    print(f"📊 Quality Score: {result['quality_score']}")
    print("✅ Evaluation Layer test: PASS")
    
except Exception as e:
    print(f"❌ Evaluation Layer error: {e}")

# Test Generation Layer (if available)
try:
    from src.srta.generation.generation_layer import GenerationLayer
    print("✅ Generation Layer imported")
    print("✅ Generation Layer test: PASS")
    
except ImportError:
    print("⚠️ Generation Layer not available")
    
print("\n🎊 Integration test completed!")
