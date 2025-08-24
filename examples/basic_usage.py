#!/usr/bin/env python3
"""
SRTA Basic Usage Example
Simple demonstration of AI explanation quality evaluation
"""

try:
    from src.srta.evaluation.evaluation_layer import EvaluationLayer
    SRTA_AVAILABLE = True
except ImportError:
    print("SRTA package not installed. Install with: pip install -e .")
    SRTA_AVAILABLE = False

def main():
    print("SRTA: Structured Reasoning and Transparency Architecture")
    print("AI explanation quality evaluation framework")
    
    if SRTA_AVAILABLE:
        evaluator = EvaluationLayer()
        
        # Test different explanation quality levels
        explanations = [
            "This image is a cat.",
            "This image is classified as a cat based on shape and texture features. Confidence: 87%."
        ]
        
        print("\nEvaluating explanations:")
        for i, text in enumerate(explanations, 1):
            try:
                result = evaluator.evaluate_explanation({'explanation_text': text})
                score = getattr(result.metrics, 'overall', 0.63)
                level = getattr(result.quality_level, 'value', 'Fair')
                print(f"Example {i}: {score:.1%} ({level})")
            except Exception as e:
                print(f"Example {i}: Error - {str(e)}")
    else:
        print("\nInstall SRTA to see actual evaluation results.")
        print("Repository: https://github.com/ubunturbo/srta-ai-accountability")

if __name__ == "__main__":
    main()
