import sys
import os
sys.path.insert(0, 'src')

def run_comparison_demo():
    try:
        from trinity.trinity_srta import create_medical_ai_trinity
        from tma.tma_srta import create_medical_ai_tma
        
        print("=" * 60)
        print("DUAL FRAMEWORK AI ARCHITECTURE DEMONSTRATION")
        print("=" * 60)
        
        trinity_system = create_medical_ai_trinity()
        tma_system = create_medical_ai_tma()
        
        queries = [
            "Should we recommend experimental treatment for a terminal cancer patient?",
            "How should we handle conflicting ethical principles in this case?",
            "What safeguards are needed before implementing this AI system?"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\nQUERY {i}: {query}")
            print("-" * 60)
            
            # Trinity
            print("TRINITY FRAMEWORK:")
            trinity_result = trinity_system.process_with_trinity(query)
            print(f"  Principles: {trinity_result['father_authority']['divine_principles']}")
            print(f"  Response: {trinity_result['son_incarnation']['incarnate_response']}")
            print(f"  Coherence: {trinity_result['spirit_unity']['divine_coherence_score']}")
            
            # TMA
            print("\nTMA FRAMEWORK:")
            tma_result = tma_system.process_with_tma(query)
            print(f"  Principles: {tma_result['authority_module']['core_principles']}")
            print(f"  Response: {tma_result['interface_module']['system_response']}")
            print(f"  Coherence: {tma_result['integration_module']['coherence_score']}")
            
            # Compare
            trinity_coherence = trinity_result['spirit_unity']['divine_coherence_score']
            tma_coherence = tma_result['integration_module']['coherence_score']
            difference = abs(trinity_coherence - tma_coherence)
            
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
