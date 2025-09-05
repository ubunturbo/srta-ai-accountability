#!/usr/bin/env python3
"""Basic functionality tests"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBasicFunctionality(unittest.TestCase):
    
    def test_imports(self):
        """Test that frameworks can be imported"""
        try:
            from three_layer.three_layer_srta import ThreeLayerSRTAArchitecture, create_medical_ai_three_layer
            from tma.tma_srta import TMAArchitecture, create_medical_ai_tma
            self.assertTrue(True, "Imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_three_layer_basic(self):
        """Test ThreeLayer framework basic functionality"""
        try:
            from three_layer.three_layer_srta import create_medical_ai_three_layer
            three_layer_ai = create_medical_ai_three_layer()
            result = three_layer_ai.process_with_three_layer("Test query")
            
            self.assertIn("authority_module", result)
            self.assertIn("mediator_module", result)
            self.assertIn("auditor_module", result)
            
        except Exception as e:
            self.fail(f"ThreeLayer test failed: {e}")
    
    def test_tma_basic(self):
        """Test TMA framework basic functionality"""
        try:
            from tma.tma_srta import create_medical_ai_tma
            tma_ai = create_medical_ai_tma()
            result = tma_ai.process_with_tma("Test query")
            
            self.assertIn("authority_module", result)
            self.assertIn("interface_module", result)
            self.assertIn("integration_module", result)
            
        except Exception as e:
            self.fail(f"TMA test failed: {e}")

if __name__ == "__main__":
    unittest.main()
