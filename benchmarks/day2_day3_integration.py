"""
SRTA Day 2-3 Integration Test
Generation Layer + Evaluation Layer Integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔄 SRTA Day 2-3 Integration Test")
print("="*50)

try:
    # Import both layers
    from src.srta.evaluation.evaluation_layer import EvaluationLayer
    print("✅ Evaluation Layer imported")
    
    try:
        from src.srta.generation.generation_layer import GenerationLayer
        print("✅ Generation Layer imported")
        generation_available = True
    except ImportError:
        print("⚠️ Generation Layer not available - using mock")
        generation_available = False
    
    # Test pipeline
    if generation_available:
        # Full pipeline test
        generator = GenerationLayer()
        evaluator = EvaluationLayer()
        
        # Mock context for generation
        gen_context = {
            'intent_analysis': {'decision': 'cat', 'confidence': 0.87},
            'original_data': {'type': 'image'},
            'style_preference': 'technical'
        }
        
        # Generate explanation
        explanation = generator.generate_explanation(gen_context)
        print(f"📝 Generated explanation: {len(explanation.get('explanation_text', ''))} chars")
        
        # Evaluate explanation
        eval_result = evaluator.evaluate_explanation(explanation)
        print(f"📊 Quality score: {eval_result.metrics.overall:.1%}")
        print(f"🏆 Quality level: {eval_result.quality_level.value}")
        
        print("\n🎊 Full Day 2-3 Integration Successful!")
        
    else:
        # Evaluation only test
        evaluator = EvaluationLayer()
        mock_explanation = {
            'explanation_text': 'This is a mock generated explanation for testing.'
        }
        
        result = evaluator.evaluate_explanation(mock_explanation)
        print(f"📊 Quality score: {result.metrics.overall:.1%}")
        print("✅ Evaluation Layer standalone test successful!")

except Exception as e:
    print(f"❌ Integration test error: {e}")
    import traceback
    traceback.print_exc()

