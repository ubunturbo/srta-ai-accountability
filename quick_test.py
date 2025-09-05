#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, 'src')

def test_frameworks():
    try:
        print("Testing Trinity framework...")
        from trinity.trinity_srta import create_medical_ai_trinity
        trinity_ai = create_medical_ai_trinity()
        trinity_result = trinity_ai.process_with_trinity("Should we proceed with treatment?")
        print(f"  Trinity coherence: {trinity_result['spirit_unity']['divine_coherence_score']}")
        
        print("Testing TMA framework...")
        from tma.tma_srta import create_medical_ai_tma
        tma_ai = create_medical_ai_tma()
        tma_result = tma_ai.process_with_tma("Should we proceed with treatment?")
        print(f"  TMA coherence: {tma_result['integration_module']['coherence_score']}")
        
        print("✅ Both frameworks working!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        return False

if __name__ == "__main__":
    test_frameworks()
