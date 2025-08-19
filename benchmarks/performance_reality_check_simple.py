#!/usr/bin/env python3
import time
import sys
import os
from datetime import datetime

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from srta.intent.intent_layer import IntentLayer, DesignPrinciple
    print("SRTA Intent Layer imported successfully!")
    
    # Quick test
    intent = IntentLayer()
    intent.add_design_principle("test", "Team", 0.5, "Test principle")
    
    print(f"Intent Layer created with {len(intent.principles)} principles")
    print("SUCCESS: SRTA Intent Layer MVP is working!")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")
