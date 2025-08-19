#!/usr/bin/env python3
"""
Unit tests for SRTA Intent Layer
"""

import pytest
from datetime import datetime
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from srta.intent.intent_layer import IntentLayer, DesignPrinciple


class TestDesignPrinciple:
    def test_principle_creation(self):
        principle = DesignPrinciple(
            "test_principle", 
            "Test Team", 
            0.5, 
            "Test justification"
        )
        assert principle.name == "test_principle"
        assert principle.stakeholder == "Test Team"
        assert principle.weight == 0.5
        assert principle.justification == "Test justification"
        assert isinstance(principle.created_at, datetime)


class TestIntentLayer:
    def test_intent_layer_creation(self):
        intent = IntentLayer()
        assert len(intent.principles) == 0
        assert len(intent.stakeholder_map) == 0
        assert isinstance(intent.created_at, datetime)
    
    def test_add_design_principle(self):
        intent = IntentLayer()
        success = intent.add_design_principle(
            "fairness", "AI Ethics Team", 0.9, "EU AI Act compliance"
        )
        assert success == True
        assert "fairness" in intent.principles
        assert "AI Ethics Team" in intent.stakeholder_map
        assert "fairness" in intent.stakeholder_map["AI Ethics Team"]
    
    def test_invalid_weight_rejected(self):
        intent = IntentLayer()
        success = intent.add_design_principle(
            "invalid", "Test Team", 1.5, "Invalid weight"
        )
        assert success == False
        assert "invalid" not in intent.principles
    
    def test_get_applicable_principles(self):
        intent = IntentLayer()
        intent.add_design_principle("test1", "Team1", 0.5, "Test 1")
        intent.add_design_principle("test2", "Team2", 0.3, "Test 2")
        
        principles = intent.get_applicable_principles()
        assert len(principles) == 2
        
    def test_stakeholder_responsibilities(self):
        intent = IntentLayer()
        intent.add_design_principle("principle1", "Team A", 0.5, "Test")
        intent.add_design_principle("principle2", "Team A", 0.3, "Test")
        intent.add_design_principle("principle3", "Team B", 0.2, "Test")
        
        team_a_responsibilities = intent.get_stakeholder_responsibilities("Team A")
        assert len(team_a_responsibilities) == 2
        assert "principle1" in team_a_responsibilities
        assert "principle2" in team_a_responsibilities
        
        team_b_responsibilities = intent.get_stakeholder_responsibilities("Team B")
        assert len(team_b_responsibilities) == 1
        assert "principle3" in team_b_responsibilities
    
    def test_principle_consistency_validation(self):
        intent = IntentLayer()
        intent.add_design_principle("test1", "Team1", 0.6, "Test")
        intent.add_design_principle("test2", "Team2", 0.7, "Test")  # Total > 1.0
        
        validation = intent.validate_principle_consistency()
        assert validation['is_consistent'] == False
        # 浮動小数点比較を修正
        assert abs(validation['total_weight'] - 1.3) < 0.01
        assert len(validation['conflicts']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
