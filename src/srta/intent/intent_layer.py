#!/usr/bin/env python3
"""
SRTA Intent Layer - MVP Implementation
Design principle tracking and stakeholder responsibility mapping
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import json


class DesignPrinciple:
    """Individual design principle with metadata"""
    
    def __init__(self, name: str, stakeholder: str, weight: float, 
                 justification: str, created_at: Optional[datetime] = None):
        self.name = name
        self.stakeholder = stakeholder
        self.weight = weight
        self.justification = justification
        self.created_at = created_at or datetime.now()
        self.version = 1
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'stakeholder': self.stakeholder,
            'weight': self.weight,
            'justification': self.justification,
            'created_at': self.created_at.isoformat(),
            'version': self.version
        }


class IntentLayer:
    """
    SRTA Intent Layer - MVP Implementation
    
    Manages design principles, stakeholder responsibilities,
    and policy tracking for AI decision accountability.
    """
    
    def __init__(self):
        self.principles: Dict[str, DesignPrinciple] = {}
        self.stakeholder_map: Dict[str, List[str]] = {}
        self.policy_registry: Dict[str, Any] = {}
        self.created_at = datetime.now()
        
    def add_design_principle(self, name: str, stakeholder: str, 
                           weight: float, justification: str) -> bool:
        """Add a new design principle with stakeholder responsibility"""
        try:
            if not (0.0 <= weight <= 1.0):
                raise ValueError("Weight must be between 0.0 and 1.0")
            
            principle = DesignPrinciple(name, stakeholder, weight, justification)
            self.principles[name] = principle
            
            # Update stakeholder mapping
            if stakeholder not in self.stakeholder_map:
                self.stakeholder_map[stakeholder] = []
            self.stakeholder_map[stakeholder].append(name)
            
            return True
            
        except Exception as e:
            print(f"Error adding design principle: {e}")
            return False
    
    def get_applicable_principles(self, context: Dict[str, Any] = None) -> List[DesignPrinciple]:
        """Get principles applicable to given context"""
        # MVP: Return all principles (filtering logic to be added later)
        return list(self.principles.values())
    
    def get_stakeholder_responsibilities(self, stakeholder: str) -> List[str]:
        """Get all principles assigned to a stakeholder"""
        return self.stakeholder_map.get(stakeholder, [])
    
    def validate_principle_consistency(self) -> Dict[str, Any]:
        """Validate consistency of design principles"""
        validation_result = {
            'is_consistent': True,
            'total_weight': 0.0,
            'conflicts': [],
            'warnings': []
        }
        
        # Check total weight distribution
        total_weight = sum(p.weight for p in self.principles.values())
        validation_result['total_weight'] = total_weight
        
        if total_weight > 1.0:
            validation_result['is_consistent'] = False
            validation_result['conflicts'].append(
                f"Total principle weights exceed 1.0: {total_weight:.2f}"
            )
        
        # Check for duplicate stakeholder assignments (warning only)
        stakeholder_counts = {}
        for stakeholder, principles in self.stakeholder_map.items():
            stakeholder_counts[stakeholder] = len(principles)
            if len(principles) > 3:  # Arbitrary threshold
                validation_result['warnings'].append(
                    f"Stakeholder '{stakeholder}' responsible for {len(principles)} principles"
                )
        
        return validation_result
    
    def export_principles(self) -> str:
        """Export principles as JSON for audit trail"""
        export_data = {
            'intent_layer_created': self.created_at.isoformat(),
            'principles': [p.to_dict() for p in self.principles.values()],
            'stakeholder_map': self.stakeholder_map,
            'validation': self.validate_principle_consistency()
        }
        return json.dumps(export_data, indent=2)
    
    def __str__(self) -> str:
        return f"IntentLayer({len(self.principles)} principles, {len(self.stakeholder_map)} stakeholders)"


# Example usage and testing
if __name__ == "__main__":
    # Create intent layer
    intent = IntentLayer()
    
    # Add sample design principles
    intent.add_design_principle(
        "fairness", 
        "AI Ethics Team", 
        0.9, 
        "Ensure equal treatment per EU AI Act Article 7"
    )
    
    intent.add_design_principle(
        "accuracy", 
        "ML Engineering Team", 
        0.8, 
        "Maintain high prediction quality for business value"
    )
    
    intent.add_design_principle(
        "transparency", 
        "Legal Team", 
        0.7, 
        "Provide explainable decisions for regulatory compliance"
    )
    
    # Test basic functionality
    print("SRTA Intent Layer MVP Test")
    print("=" * 40)
    print(f"Intent Layer: {intent}")
    print(f"Applicable Principles: {len(intent.get_applicable_principles())}")
    print(f"AI Ethics Team Responsibilities: {intent.get_stakeholder_responsibilities('AI Ethics Team')}")
    
    # Validate consistency
    validation = intent.validate_principle_consistency()
    print(f"Consistency Check: {'PASS' if validation['is_consistent'] else 'FAIL'}")
    if validation['conflicts']:
        for conflict in validation['conflicts']:
            print(f"  WARNING: {conflict}")
    
    # Export for audit
    print("\nAudit Trail Export:")
    print(intent.export_principles())
    
    print("\nIntent Layer MVP working!")
