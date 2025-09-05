#!/usr/bin/env python3
"""Simple Test for SRTA Components"""

import sys
import os

print("Testing SRTA component imports...")

try:
    from evaluation_layer_enhanced_v2 import EnhancedSRTAEvaluationLayer
    print("✓ evaluation_layer_enhanced_v2 import successful")
except ImportError as e:
    print(f"✗ evaluation_layer_enhanced_v2 import failed: {e}")

try:
    from responsibility_tracker_enhanced import EnhancedResponsibilityTracker  
    print("✓ responsibility_tracker_enhanced import successful")
except ImportError as e:
    print(f"✗ responsibility_tracker_enhanced import failed: {e}")

print("Component test complete.")
