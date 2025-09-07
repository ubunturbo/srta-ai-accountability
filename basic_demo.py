#!/usr/bin/env python3
"""
Basic demonstration of SRTA evaluation functionality
"""
try:
    from src.srta.evaluation.evaluation_layer import EvaluationLayer, EvaluationResult
    from src.tma.tma_srta import TMAArchitecture
    
    print("=== SRTA Basic Demo ===")
    
    # Initialize components
    evaluator = EvaluationLayer()
    tma = TMAArchitecture()
    
    # Simple test case
    test_explanation = {
        'text': 'The model predicted class A based on feature X having high importance.',
        'context': 'medical_diagnosis'
    }
    
    print(f"Testing explanation: {test_explanation['text']}")
    
    # This would need to be adapted based on actual method signatures
    # but shows the structure for real functionality
    print("✓ Components initialized successfully")
    print("✓ Basic demo completed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
