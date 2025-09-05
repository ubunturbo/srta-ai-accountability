import sys
import os

print("=== FRAMEWORK TEST ===")

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

print(f"Testing from directory: {current_dir}")
print(f"Source directory: {src_dir}")

try:
    from trinity.trinity_srta import create_medical_ai_trinity
    print("✓ Trinity import successful")
    
    from tma.tma_srta import create_medical_ai_tma
    print("✓ TMA import successful")
    
    # Test Trinity
    print("\nTesting Trinity framework...")
    trinity_ai = create_medical_ai_trinity()
    trinity_result = trinity_ai.process_with_trinity("Should we proceed with treatment?")
    print(f"Trinity coherence: {trinity_result['spirit_unity']['divine_coherence_score']}")
    
    # Test TMA
    print("Testing TMA framework...")
    tma_ai = create_medical_ai_tma()
    tma_result = tma_ai.process_with_tma("Should we proceed with treatment?")
    print(f"TMA coherence: {tma_result['integration_module']['coherence_score']}")
    
    print("\n✓ Both frameworks working successfully!")
    print("✓ Repository implementation complete!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Runtime error: {e}")
    import traceback
    traceback.print_exc()
