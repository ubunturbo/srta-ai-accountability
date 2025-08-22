#!/usr/bin/env python3
"""
SRTA Intent Layer - MVP Implementation
Design principle tracking and stakeholder responsibility mapping

SRTA Intent Layer - MVP実装
設計原則追跡とステークホルダー責任マッピング
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import json


class DesignPrinciple:
    """
    Individual design principle with metadata.
    メタデータを持つ個別の設計原則。
    
    Core component for storing design rationale required for
    formal causation analysis and "why" question answering.
    
    形式的因果関係分析と「なぜ」質問回答に必要な
    設計根拠を保存するための核心コンポーネント。
    """

    def __init__(self, name: str, stakeholder: str, weight: float,
                 justification: str, created_at: Optional[datetime] = None):
        self.name = name                                    # Principle name
        self.stakeholder = stakeholder                      # Responsible party
        self.weight = weight                               # Importance weight (0-1)
        self.justification = justification                 # Design rationale
        self.created_at = created_at or datetime.now()     # Creation timestamp
        self.version = 1                                   # Version number

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
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
    SRTA Intent Layer - MVP実装

    Manages design principles, stakeholder responsibilities,
    and policy tracking for AI decision accountability.
    
    AI決定責任のための設計原則、ステークホルダー責任、
    ポリシー追跡を管理します。
    """

    def __init__(self):
        self.principles: Dict[str, DesignPrinciple] = {}    # Stored design principles
        self.stakeholder_map: Dict[str, List[str]] = {}     # Stakeholder-principle mapping
        self.policy_registry: Dict[str, Any] = {}           # Policy registry
        self.created_at = datetime.now()                    # Creation timestamp

    def add_design_principle(self, name: str, stakeholder: str,
                           weight: float, justification: str) -> bool:
        """
        Add a design principle to the Intent Layer.
        Intent Layerに設計原則を追加。

        Enables systematic storage of design rationale required for
        formal causation analysis and "why" question answering.
        
        形式的因果関係分析と「なぜ」質問回答に必要な
        設計根拠の体系的保存を可能にします。

        Args:
            name: Principle name
            stakeholder: Responsible party  
            weight: Importance weight (0-1)
            justification: Design rationale

        Returns:
            bool: Success status
        """
        try:
            principle = DesignPrinciple(name, stakeholder, weight, justification)
            
            # Store principle
            principle_id = f"principle_{len(self.principles)}"
            self.principles[principle_id] = principle
            
            # Update stakeholder mapping
            if stakeholder not in self.stakeholder_map:
                self.stakeholder_map[stakeholder] = []
            self.stakeholder_map[stakeholder].append(principle_id)
            
            return True
            
        except Exception as e:
            print(f"Error adding design principle: {e}")
            return False

    def get_principles_by_stakeholder(self, stakeholder: str) -> List[DesignPrinciple]:
        """Get all principles associated with a stakeholder."""
        if stakeholder not in self.stakeholder_map:
            return []
        
        principles = []
        for principle_id in self.stakeholder_map[stakeholder]:
            if principle_id in self.principles:
                principles.append(self.principles[principle_id])
        
        return principles

    def get_all_principles(self) -> Dict[str, DesignPrinciple]:
        """Get all stored design principles."""
        return self.principles.copy()

    def calculate_stakeholder_influence(self, stakeholder: str) -> float:
        """Calculate total influence of a stakeholder based on their principles."""
        principles = self.get_principles_by_stakeholder(stakeholder)
        if not principles:
            return 0.0
        
        total_weight = sum(p.weight for p in principles)
        return min(1.0, total_weight / len(principles))

    def analyze_principle_compliance(self, input_data: Any) -> Dict[str, Any]:
        """
        Analyze compliance of input against stored design principles.
        保存された設計原則に対する入力のコンプライアンス分析。

        Provides foundation for "why" question answering by linking
        decisions to design rationale and stakeholder responsibilities.
        
        決定を設計根拠とステークホルダー責任に結び付けることで
        「なぜ」質問回答の基盤を提供します。
        """
        analysis = {
            'applicable_principles': [],
            'stakeholder_attribution': {},
            'compliance_score': 0.0,
            'recommendation_confidence': 0.0
        }

        # Find applicable principles
        applicable_principles = []
        for principle_id, principle in self.principles.items():
            relevance = self._calculate_principle_relevance(principle, input_data)
            if relevance > 0.3:
                applicable_principles.append({
                    'id': principle_id,
                    'principle': principle,
                    'relevance': relevance
                })

        if not applicable_principles:
            return analysis

        # Calculate analysis metrics
        total_weight = 0.0
        stakeholder_weights = {}

        for item in applicable_principles:
            principle = item['principle']
            relevance = item['relevance']
            weighted_score = principle.weight * relevance

            analysis['applicable_principles'].append({
                'name': principle.name,
                'stakeholder': principle.stakeholder,
                'weight': principle.weight,
                'relevance': relevance,
                'justification': principle.justification
            })

            # Track stakeholder attribution
            if principle.stakeholder not in stakeholder_weights:
                stakeholder_weights[principle.stakeholder] = 0.0
            stakeholder_weights[principle.stakeholder] += weighted_score
            total_weight += weighted_score

        # Normalize stakeholder attribution
        if total_weight > 0:
            for stakeholder, weight in stakeholder_weights.items():
                analysis['stakeholder_attribution'][stakeholder] = weight / total_weight
            
            analysis['compliance_score'] = min(1.0, total_weight / len(applicable_principles))
            analysis['recommendation_confidence'] = min(1.0, total_weight)

        return analysis

    def _calculate_principle_relevance(self, principle: DesignPrinciple, 
                                     input_data: Any) -> float:
        """Calculate relevance of principle to input data."""
        relevance = principle.weight * 0.5  # Base relevance
        
        # Simple keyword matching for demonstration
        input_str = str(input_data).lower()
        principle_keywords = principle.name.lower().split()
        
        for keyword in principle_keywords:
            if keyword in input_str:
                relevance += 0.2
        
        return min(1.0, relevance)

    def export_state(self) -> Dict[str, Any]:
        """Export complete Intent Layer state."""
        return {
            'principles': {pid: p.to_dict() for pid, p in self.principles.items()},
            'stakeholder_map': self.stakeholder_map,
            'policy_registry': self.policy_registry,
            'created_at': self.created_at.isoformat(),
            'total_principles': len(self.principles),
            'total_stakeholders': len(self.stakeholder_map)
        }

    def load_state(self, state_data: Dict[str, Any]) -> bool:
        """Load Intent Layer state from exported data."""
        try:
            # Clear current state
            self.principles.clear()
            self.stakeholder_map.clear()
            
            # Load principles
            for principle_id, principle_data in state_data['principles'].items():
                principle = DesignPrinciple(
                    name=principle_data['name'],
                    stakeholder=principle_data['stakeholder'],
                    weight=principle_data['weight'],
                    justification=principle_data['justification'],
                    created_at=datetime.fromisoformat(principle_data['created_at'])
                )
                self.principles[principle_id] = principle
            
            # Load stakeholder mapping
            self.stakeholder_map = state_data['stakeholder_map']
            self.policy_registry = state_data.get('policy_registry', {})
            
            return True
            
        except Exception as e:
            print(f"Error loading state: {e}")
            return False


# Demonstration and testing
if __name__ == "__main__":
    """
    Demonstration of Intent Layer capabilities.
    Intent Layer能力のデモンストレーション。
    """
    
    print("SRTA Intent Layer - MVP Implementation")
    print("SRTA Intent Layer - MVP実装")
    print("=" * 50)
    
    # Initialize Intent Layer
    intent_layer = IntentLayer()
    print("Intent Layer initialized")
    print("Intent Layer初期化完了")
    
    # Add sample design principles
    print("\nAdding design principles...")
    print("設計原則を追加中...")
    
    success1 = intent_layer.add_design_principle(
        "Data Privacy Protection",
        "Data Protection Officer", 
        0.9,
        "Protect user privacy according to GDPR Article 5"
    )
    
    success2 = intent_layer.add_design_principle(
        "Algorithmic Fairness",
        "AI Ethics Committee",
        0.85, 
        "Prevent bias and ensure equitable treatment"
    )
    
    success3 = intent_layer.add_design_principle(
        "Transparency Requirement", 
        "Regulatory Compliance Team",
        0.95,
        "Provide clear explanations as required by EU AI Act"
    )
    
    print(f"Added principles: {success1}, {success2}, {success3}")
    print(f"原則追加結果: {success1}, {success2}, {success3}")
    
    # Demonstrate analysis
    sample_input = {
        "user_data": "sensitive medical information",
        "decision_type": "treatment recommendation", 
        "risk_level": "high"
    }
    
    print(f"\nAnalyzing sample input: {sample_input}")
    print(f"サンプル入力の分析: {sample_input}")
    
    analysis_result = intent_layer.analyze_principle_compliance(sample_input)
    
    print(f"\nCompliance Analysis Results:")
    print(f"コンプライアンス分析結果:")
    print(f"Applicable principles: {len(analysis_result['applicable_principles'])}")
    print(f"適用可能原則数: {len(analysis_result['applicable_principles'])}")
    print(f"Compliance score: {analysis_result['compliance_score']:.2f}")
    print(f"コンプライアンススコア: {analysis_result['compliance_score']:.2f}")
    print(f"Stakeholder attribution: {analysis_result['stakeholder_attribution']}")
    print(f"ステークホルダー帰属: {analysis_result['stakeholder_attribution']}")
    
    # Export state for verification
    exported_state = intent_layer.export_state()
    print(f"\nTotal principles stored: {exported_state['total_principles']}")
    print(f"保存された総原則数: {exported_state['total_principles']}")
    print(f"Total stakeholders: {exported_state['total_stakeholders']}")
    print(f"総ステークホルダー数: {exported_state['total_stakeholders']}")
