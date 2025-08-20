import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🚀 SRTA Simple Test")
try:
    from src.srta.evaluation.evaluation_layer import EvaluationLayer
    evaluator = EvaluationLayer()
    result = evaluator.evaluate_explanation({})
    print("✅ Test successful!")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
