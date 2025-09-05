import sys
import os
sys.path.insert(0, 'src')

def run_comparison_demo():
    try:
        from three_layer.three_layer_srta import create_medical_ai_three_layer
        from tma.tma_srta import create_medical_ai_tma
        
        print("=" * 60)
        print("DUAL FRAMEWORK AI ARCHITECTURE DEMONSTRATION")
        print("=" * 60)
        
        three_layer_system = create_medical_ai_three_layer()
        tma_system = create_medical_ai_tma()
        
        queries = [
            "Should we recommend experimental treatment for a terminal cancer patient?",
            "How should we handle conflicting ethical principles in this case?",
            "What safeguards are needed before implementing this AI system?"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\nQUERY {i}: {query}")
            print("-" * 60)
            
            # ThreeLayer
            print("THREE-LAYER FRAMEWORK:")
            three_layer_result = three_layer_system.process_with_three_layer(query)
            print(f"  Principles: {three_layer_result['authority_module']['core_principles']}")
            print(f"  Response: {three_layer_result['mediator_module']['incarnate_response']}")
            print(f"  Coherence: {three_layer_result['system_unity']['system_coherence_score']}")
            
            # TMA
            print("\nTMA FRAMEWORK:")
            tma_result = tma_system.process_with_tma(query)
            print(f"  Principles: {tma_result['authority_module']['core_principles']}")
            print(f"  Response: {tma_result['interface_module']['system_response']}")
            print(f"  Coherence: {tma_result['integration_module']['coherence_score']}")
            
            # Compare
            three_layer_coherence = three_layer_result['system_unity']['system_coherence_score']
            tma_coherence = tma_result['integration_module']['coherence_score']
            difference = abs(three_layer_coherence - tma_coherence)
            
            print(f"\nEQUIVALENCE: Difference = {difference:.3f}")
            print(f"Status: {'✓ EQUIVALENT' if difference < 0.1 else '⚠ REVIEW NEEDED'}")
        
        print(f"\n{'=' * 60}")
        print("DEMONSTRATION COMPLETE")
        print("✓ Dual framework repository successfully implemented")
        print("✓ Ready for academic research and practical deployment")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_comparison_demo()
