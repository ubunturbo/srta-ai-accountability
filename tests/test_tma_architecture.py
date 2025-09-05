# テストファイル作成のためのコマンド
cat > tests/test_tma_architecture.py << 'EOF'
#!/usr/bin/env python3
"""
TMA-SRTA Architecture Test Suite
Comprehensive testing for Three-Module Architecture implementation
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from datetime import datetime
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tma.tma_srta import (
    TMAArchitecture, 
    AuthorityModule, 
    InterfaceModule, 
    IntegrationModule,
    DesignPrinciple, 
    ProcessingContext
)

class TestTMAArchitecture:
    """Test complete TMA Architecture integration"""
    
    @pytest.fixture
    def sample_principles(self):
        return [
            DesignPrinciple(
                name="transparency",
                description="All decisions must be explainable and auditable",
                weight=0.85,
                constraints={"audit_trail": True, "explanation_required": True},
                stakeholder_input={"users": 0.6, "regulators": 0.4}
            ),
            DesignPrinciple(
                name="safety",
                description="Safety considerations override efficiency",
                weight=0.90,
                constraints={"safety_check": True, "human_oversight": True},
                stakeholder_input={"safety_committee": 0.7, "operators": 0.3}
            )
        ]
    
    @pytest.fixture
    def tma_system(self, sample_principles):
        return TMAArchitecture(sample_principles, "Test TMA System")
    
    def test_tma_initialization(self, sample_principles):
        """Test TMA Architecture initialization"""
        tma = TMAArchitecture(sample_principles, "Test System")
        
        assert tma.system_purpose == "Test System"
        assert isinstance(tma.authority, AuthorityModule)
        assert isinstance(tma.interface, InterfaceModule)
        assert isinstance(tma.integration, IntegrationModule)
        assert len(tma.authority.principles) == 2
        assert tma.processing_history == []
    
    def test_process_with_tma(self, tma_system):
        """Test complete TMA processing pipeline"""
        query = "Process a complex decision requiring safety and transparency considerations"
        result = tma_system.process_with_tma(query)
        
        # Verify complete result structure
        assert "authority_principles" in result
        assert "interface_mediation" in result  
        assert "integration_validation" in result
        assert "system_metadata" in result
        
        # Verify coherence score is reasonable
        coherence = result["integration_validation"]["coherence_score"]
        assert isinstance(coherence, float)
        assert 0.0 <= coherence <= 1.0
    
    def test_explain_decision(self, tma_system):
        """Test decision explanation functionality"""
        query = "Explain this decision process"
        explanation = tma_system.explain_decision(query)
        
        # Verify explanation structure
        expected_keys = ["what", "why", "how", "validation", "accountability"]
        for key in expected_keys:
            assert key in explanation
            assert isinstance(explanation[key], str)
            assert len(explanation[key]) > 0

def test_module_imports():
    """Test that all required modules can be imported"""
    from tma.tma_srta import TMAArchitecture
    from tma.tma_srta import AuthorityModule
    from tma.tma_srta import InterfaceModule  
    from tma.tma_srta import IntegrationModule
    from tma.tma_srta import DesignPrinciple
    from tma.tma_srta import ProcessingContext
    
    # All imports successful
    assert True

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"])
EOF
