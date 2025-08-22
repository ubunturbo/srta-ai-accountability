"""
SRTA Generation Layer
AI決定の説明文を生成する基本クラス

SRTA Generation Layer  
Basic class for generating AI decision explanations
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class ExplanationStyle(Enum):
    """
    Explanation style types.
    説明スタイルの種類。
    """
    SIMPLE = "simple"       # Simple explanation / シンプルな説明
    DETAILED = "detailed"   # Detailed explanation / 詳細な説明
    TECHNICAL = "technical" # Technical explanation / 技術的な説明


@dataclass
class GenerationContext:
    """
    Context information for explanation generation.
    説明生成のコンテキスト情報。
    
    Configures how explanations are generated to meet different
    user needs and regulatory requirements.
    
    異なるユーザーニーズと規制要件を満たすために
    説明の生成方法を設定します。
    """
    user_background: str = "general"                         # User knowledge level / ユーザーの背景知識レベル
    explanation_style: ExplanationStyle = ExplanationStyle.SIMPLE  # Style preference / スタイル設定
    max_length: int = 200                                   # Maximum characters / 最大文字数
    include_confidence: bool = True                         # Include confidence score / 信頼度を含めるか
    language: str = "ja"                                    # Language setting / 言語設定


@dataclass
class GeneratedExplanation:
    """
    Generated explanation results.
    生成された説明の結果。
    
    Contains complete explanation with metadata for
    accountability and audit requirements.
    
    責任追跡と監査要件のためのメタデータを含む
    完全な説明を格納します。
    """
    main_explanation: str                  # Primary explanation text
    confidence_score: float               # Confidence level (0-1)
    reasoning_steps: List[str]            # Step-by-step reasoning
    metadata: Dict[str, Any]              # Additional metadata
    generation_timestamp: str             # Generation time


class GenerationLayer:
    """
    Main class for generating AI decision explanations.
    AI決定の説明文を生成するメインクラス。
    
    Receives analysis results from Intent Layer and converts them
    into human-readable explanations that address regulatory
    transparency requirements.
    
    Intent Layerからの分析結果を受け取り、規制の
    透明性要件に対応する人間が理解しやすい説明に変換します。
    """

    def __init__(self, context: Optional[GenerationContext] = None):
        """
        Initialize Generation Layer.
        Generation Layerを初期化。

        Args:
            context: Generation configuration / 生成設定
        """
        self.context = context or GenerationContext()
        self.explanation_templates = self._load_explanation_templates()
        self.generation_count = 0

        print("SRTA Generation Layer initialized")
        print("SRTA Generation Layer初期化完了")

    def _load_explanation_templates(self) -> Dict[str, str]:
        """Load explanation templates for different styles."""
        return {
            'simple': "The system decided {decision} because {main_reason}. Confidence: {confidence}%",
            'detailed': "Based on analysis of {input_summary}, the system made decision: {decision}. "
                       "Primary reasoning: {main_reason}. Supporting factors: {supporting_factors}. "
                       "Confidence level: {confidence}%",
            'technical': "Decision Process: {decision} | Input Analysis: {input_summary} | "
                        "Applied Principles: {principles} | Confidence Score: {confidence} | "
                        "Processing Time: {processing_time}ms"
        }

    def generate_explanation(self, analysis_result: Dict[str, Any], 
                           input_data: Any, decision: Any) -> GeneratedExplanation:
        """
        Generate human-readable explanation from analysis results.
        分析結果から人間が読める説明を生成。

        Core method implementing Trinity-inspired explanation synthesis,
        combining intent analysis with operational processing for
        complete accountability.
        
        Intent分析と運用処理を組み合わせて完全な責任追跡を
        実現する三位一体にインスパイアされた説明合成を実装する核心メソッド。

        Args:
            analysis_result: Intent Layer analysis / Intent Layer分析結果
            input_data: Original input / 元の入力
            decision: AI decision / AI決定

        Returns:
            GeneratedExplanation: Complete explanation / 完全な説明
        """
        self.generation_count += 1
        start_time = datetime.now()

        # Extract key components for explanation / 説明のための主要コンポーネント抽出
        main_reason = self._extract_primary_reasoning(analysis_result)
        supporting_factors = self._extract_supporting_factors(analysis_result)
        confidence = self._calculate_explanation_confidence(analysis_result)

        # Generate explanation based on style / スタイルに基づく説明生成
        explanation_text = self._format_explanation(
            decision, main_reason, supporting_factors, confidence, input_data
        )

        # Create reasoning steps / 推論ステップ作成
        reasoning_steps = self._generate_reasoning_steps(analysis_result)

        # Prepare metadata / メタデータ準備
        metadata = {
            'generation_id': self.generation_count,
            'style': self.context.explanation_style.value,
            'language': self.context.language,
            'applicable_principles': len(analysis_result.get('applicable_principles', [])),
            'stakeholder_count': len(analysis_result.get('stakeholder_attribution', {})),
            'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
        }

        return GeneratedExplanation(
            main_explanation=explanation_text,
            confidence_score=confidence,
            reasoning_steps=reasoning_steps,
            metadata=metadata,
            generation_timestamp=start_time.isoformat()
        )

    def _extract_primary_reasoning(self, analysis_result: Dict[str, Any]) -> str:
        """Extract primary reasoning from analysis results."""
        applicable_principles = analysis_result.get('applicable_principles', [])
        
        if not applicable_principles:
            return "No specific design principles identified"
        
        # Find highest weighted principle
        primary_principle = max(applicable_principles, 
                              key=lambda p: p.get('weight', 0) * p.get('relevance', 0))
        
        return f"{primary_principle['name']}: {primary_principle['justification']}"

    def _extract_supporting_factors(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Extract supporting factors from analysis."""
        factors = []
        
        # Add stakeholder information
        stakeholders = analysis_result.get('stakeholder_attribution', {})
        if stakeholders:
            primary_stakeholder = max(stakeholders.items(), key=lambda x: x[1])
            factors.append(f"Primary responsibility: {primary_stakeholder[0]} ({primary_stakeholder[1]:.2f})")
        
        # Add compliance information
        compliance_score = analysis_result.get('compliance_score', 0)
        if compliance_score > 0:
            factors.append(f"Compliance score: {compliance_score:.2f}")
        
        return factors

    def _calculate_explanation_confidence(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate confidence in the explanation."""
        confidence_factors = []
        
        # Factor 1: Number of applicable principles
        principle_count = len(analysis_result.get('applicable_principles', []))
        if principle_count > 0:
            confidence_factors.append(min(1.0, principle_count / 3))  # Normalize to max 3 principles
        
        # Factor 2: Compliance score
        compliance = analysis_result.get('compliance_score', 0)
        confidence_factors.append(compliance)
        
        # Factor 3: Recommendation confidence
        recommendation_confidence = analysis_result.get('recommendation_confidence', 0)
        confidence_factors.append(recommendation_confidence)
        
        # Calculate weighted average
        if confidence_factors:
            return sum(confidence_factors) / len(confidence_factors)
        else:
            return 0.5  # Default moderate confidence

    def _format_explanation(self, decision: Any, main_reason: str, 
                          supporting_factors: List[str], confidence: float,
                          input_data: Any) -> str:
        """Format explanation according to selected style."""
        
        template = self.explanation_templates.get(self.context.explanation_style.value, 
                                                self.explanation_templates['simple'])
        
        # Prepare formatting parameters
        format_params = {
            'decision': str(decision),
            'main_reason': main_reason,
            'confidence': int(confidence * 100),
            'input_summary': self._summarize_input(input_data),
            'supporting_factors': '; '.join(supporting_factors) if supporting_factors else 'None',
            'principles': f"{len(supporting_factors)} principles applied",
            'processing_time': self.generation_count * 10  # Simulated processing time
        }
        
        try:
            formatted_explanation = template.format(**format_params)
        except KeyError as e:
            # Fallback to simple template if formatting fails
            formatted_explanation = self.explanation_templates['simple'].format(
                decision=format_params['decision'],
                main_reason=format_params['main_reason'],
                confidence=format_params['confidence']
            )
        
        # Truncate if necessary
        if len(formatted_explanation) > self.context.max_length:
            formatted_explanation = formatted_explanation[:self.context.max_length - 3] + "..."
        
        return formatted_explanation

    def _summarize_input(self, input_data: Any) -> str:
        """Create brief summary of input data."""
        if isinstance(input_data, dict):
            key_count = len(input_data)
            return f"structured data with {key_count} fields"
        elif isinstance(input_data, (list, tuple)):
            return f"sequence data with {len(input_data)} elements"
        else:
            input_str = str(input_data)
            return input_str[:50] + "..." if len(input_str) > 50 else input_str

    def _generate_reasoning_steps(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate step-by-step reasoning explanation."""
        steps = []
        
        # Step 1: Input analysis
        steps.append("1. Analyzed input data for applicable design principles")
        
        # Step 2: Principle matching
        principle_count = len(analysis_result.get('applicable_principles', []))
        steps.append(f"2. Identified {principle_count} relevant design principles")
        
        # Step 3: Stakeholder attribution
        stakeholder_count = len(analysis_result.get('stakeholder_attribution', {}))
        if stakeholder_count > 0:
            steps.append(f"3. Attributed responsibility across {stakeholder_count} stakeholders")
        
        # Step 4: Compliance assessment
        compliance = analysis_result.get('compliance_score', 0)
        steps.append(f"4. Assessed regulatory compliance: {compliance:.2f}")
        
        # Step 5: Decision generation
        steps.append("5. Generated final decision based on weighted principle analysis")
        
        return steps

    def update_context(self, new_context: GenerationContext):
        """Update generation context settings."""
        self.context = new_context
        print(f"Generation context updated: {new_context.explanation_style.value} style")

    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get generation layer performance statistics."""
        return {
            'total_generations': self.generation_count,
            'current_style': self.context.explanation_style.value,
            'current_language': self.context.language,
            'max_length_setting': self.context.max_length,
            'templates_loaded': len(self.explanation_templates)
        }

    def export_explanation_history(self) -> Dict[str, Any]:
        """Export explanation generation history for audit."""
        return {
            'generation_count': self.generation_count,
            'context_settings': asdict(self.context),
            'available_templates': list(self.explanation_templates.keys()),
            'export_timestamp': datetime.now().isoformat()
        }


# Demonstration and testing
if __name__ == "__main__":
    """
    Demonstration of Generation Layer capabilities.
    Generation Layer能力のデモンストレーション。
    """
    
    print("SRTA Generation Layer - Explanation Generation")
    print("SRTA Generation Layer - 説明生成")
    print("=" * 50)
    
    # Initialize Generation Layer
    context = GenerationContext(
        explanation_style=ExplanationStyle.DETAILED,
        max_length=300,
        language="en"
    )
    generation_layer = GenerationLayer(context)
    
    # Sample analysis result from Intent Layer
    sample_analysis = {
        'applicable_principles': [
            {
                'name': 'Data Privacy Protection',
                'stakeholder': 'Data Protection Officer',
                'weight': 0.9,
                'relevance': 0.8,
                'justification': 'Protect user privacy according to GDPR Article 5'
            },
            {
                'name': 'Algorithmic Fairness', 
                'stakeholder': 'AI Ethics Committee',
                'weight': 0.85,
                'relevance': 0.7,
                'justification': 'Prevent bias and ensure equitable treatment'
            }
        ],
        'stakeholder_attribution': {
            'Data Protection Officer': 0.6,
            'AI Ethics Committee': 0.4
        },
        'compliance_score': 0.75,
        'recommendation_confidence': 0.8
    }
    
    sample_input = {
        'user_id': '12345',
        'data_type': 'medical',
        'request': 'treatment_recommendation'
    }
    
    sample_decision = 0.75  # Approval score
    
    print("Generating explanation...")
    print("説明を生成中...")
    
    # Generate explanation
    explanation = generation_layer.generate_explanation(
        sample_analysis, sample_input, sample_decision
    )
    
    print(f"\nGenerated Explanation:")
    print(f"生成された説明:")
    print(f"Main: {explanation.main_explanation}")
    print(f"Confidence: {explanation.confidence_score:.2f}")
    print(f"Steps: {len(explanation.reasoning_steps)}")
    
    print(f"\nReasoning Steps:")
    print(f"推論ステップ:")
    for step in explanation.reasoning_steps:
        print(f"  {step}")
    
    print(f"\nMetadata:")
    print(f"メタデータ:")
    for key, value in explanation.metadata.items():
        print(f"  {key}: {value}")
    
    # Test different styles
    print(f"\nTesting different explanation styles...")
    print(f"異なる説明スタイルをテスト中...")
    
    for style in ExplanationStyle:
        context.explanation_style = style
        generation_layer.update_context(context)
        
        test_explanation = generation_layer.generate_explanation(
            sample_analysis, sample_input, sample_decision
        )
        
        print(f"\n{style.value}: {test_explanation.main_explanation}")
    
    # Performance statistics
    stats = generation_layer.get_generation_statistics()
    print(f"\nGeneration Statistics:")
    print(f"生成統計:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
