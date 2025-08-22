"""
SRTA Evaluation Layer - Quality Assessment Module (Enhanced Version)
SRTA評価レイヤー - 品質評価モジュール（拡張版）

Evaluates explanation quality and provides improvement recommendations
for accountability and regulatory compliance.

責任追跡と規制遵守のための説明品質評価と改善推奨を提供します。
"""

import time
import re
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class QualityLevel(Enum):
    """
    Quality assessment levels for explanations.
    説明の品質評価レベル。
    """
    EXCELLENT = "Excellent"  # 90%+ quality score
    GOOD = "Good"           # 75-89% quality score  
    FAIR = "Fair"           # 60-74% quality score
    POOR = "Poor"           # <60% quality score


@dataclass
class EvaluationMetrics:
    """
    Comprehensive evaluation metrics for explanation quality.
    説明品質の包括的評価指標。
    
    Provides quantitative assessment required for regulatory
    compliance and audit requirements.
    
    規制遵守と監査要件に必要な定量的評価を提供します。
    """
    clarity: float = 0.0            # Text clarity score (0-1)
    completeness: float = 0.0       # Information completeness (0-1)
    understandability: float = 0.0  # User comprehension level (0-1) 
    overall: float = 0.0            # Overall quality score (0-1)


@dataclass
class EvaluationResult:
    """
    Complete evaluation result with metrics and recommendations.
    指標と推奨を含む完全な評価結果。
    
    Supports accountability reporting and continuous improvement
    of explanation quality.
    
    責任報告と説明品質の継続的改善をサポートします。
    """
    metrics: EvaluationMetrics          # Quantitative metrics
    quality_level: QualityLevel         # Overall quality assessment
    improvement_suggestions: List[str]  # Specific recommendations
    assessment_message: str             # Human-readable summary
    processing_time: float              # Evaluation processing time


class EvaluationLayer:
    """
    Enhanced quality assessment module for SRTA explanations.
    SRTA説明の拡張品質評価モジュール。
    
    Implements comprehensive evaluation supporting regulatory compliance
    requirements and continuous improvement of explanation quality.
    
    規制遵守要件と説明品質の継続的改善をサポートする
    包括的評価を実装します。
    """

    def __init__(self):
        self.quality_thresholds = {
            QualityLevel.EXCELLENT: 0.9,   # 90%+ threshold
            QualityLevel.GOOD: 0.75,       # 75-89% threshold
            QualityLevel.FAIR: 0.6,        # 60-74% threshold
            QualityLevel.POOR: 0.4         # <60% threshold
        }
        
        # Enhanced evaluation criteria
        self.evaluation_criteria = {
            'clarity': {
                'sentence_length': {'max': 25, 'weight': 0.3},
                'jargon_usage': {'max_ratio': 0.1, 'weight': 0.4},
                'readability': {'min_score': 0.7, 'weight': 0.3}
            },
            'completeness': {
                'what_coverage': {'required': True, 'weight': 0.25},
                'why_coverage': {'required': True, 'weight': 0.25},
                'how_coverage': {'required': True, 'weight': 0.25},
                'who_coverage': {'required': True, 'weight': 0.25}
            },
            'understandability': {
                'explanation_length': {'min': 50, 'max': 500, 'weight': 0.4},
                'structure_clarity': {'weight': 0.3},
                'context_appropriateness': {'weight': 0.3}
            }
        }
        
        self.evaluation_count = 0
        print("SRTA Evaluation Layer (Enhanced Quality Assessment Module) initialized")

    def evaluate_explanation(self, context: Dict[str, Any]) -> EvaluationResult:
        """
        Comprehensive evaluation of explanation quality.
        説明品質の包括的評価。

        Performs multi-dimensional quality assessment supporting
        regulatory compliance and accountability requirements.
        
        規制遵守と責任要件をサポートする
        多次元品質評価を実行します。

        Args:
            context: Evaluation context including explanation text

        Returns:
            EvaluationResult: Complete evaluation with recommendations
        """
        start_time = time.time()
        self.evaluation_count += 1

        # Extract explanation text
        text = context.get('explanation_text', '')
        generated_explanation = context.get('generated_explanation')
        
        if generated_explanation:
            text = generated_explanation.main_explanation
            confidence = generated_explanation.confidence_score
            metadata = generated_explanation.metadata
        else:
            confidence = context.get('confidence', 0.5)
            metadata = {}

        # Calculate comprehensive metrics
        clarity = self._evaluate_clarity(text)
        completeness = self._evaluate_completeness(text, context)
        understandability = self._evaluate_understandability(text, context)
        
        # Calculate overall score with weighting
        overall = self._calculate_overall_score(clarity, completeness, understandability, confidence)
        
        # Create metrics object
        metrics = EvaluationMetrics(
            clarity=clarity,
            completeness=completeness, 
            understandability=understandability,
            overall=overall
        )
        
        # Determine quality level
        quality_level = self._determine_quality_level(overall)
        
        # Generate improvement suggestions
        suggestions = self._generate_improvement_suggestions(metrics, context)
        
        # Create assessment message
        assessment_message = self._create_assessment_message(quality_level, overall, len(suggestions))
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return EvaluationResult(
            metrics=metrics,
            quality_level=quality_level,
            improvement_suggestions=suggestions,
            assessment_message=assessment_message,
            processing_time=processing_time
        )

    def _evaluate_clarity(self, text: str) -> float:
        """Evaluate text clarity using multiple criteria."""
        if not text:
            return 0.0
        
        clarity_scores = []
        
        # Sentence length analysis
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len([s for s in sentences if s.strip()])
            max_length = self.evaluation_criteria['clarity']['sentence_length']['max']
            length_score = max(0, 1 - (avg_sentence_length - max_length) / max_length) if avg_sentence_length > max_length else 1.0
            clarity_scores.append(length_score * self.evaluation_criteria['clarity']['sentence_length']['weight'])
        
        # Jargon usage analysis
        jargon_words = ['algorithm', 'heuristic', 'optimization', 'neural', 'computational']
        word_count = len(text.split())
        jargon_count = sum(1 for word in text.lower().split() if any(jargon in word for jargon in jargon_words))
        jargon_ratio = jargon_count / word_count if word_count > 0 else 0
        max_jargon_ratio = self.evaluation_criteria['clarity']['jargon_usage']['max_ratio']
        jargon_score = max(0, 1 - (jargon_ratio - max_jargon_ratio) / max_jargon_ratio) if jargon_ratio > max_jargon_ratio else 1.0
        clarity_scores.append(jargon_score * self.evaluation_criteria['clarity']['jargon_usage']['weight'])
        
        # Basic readability (simplified)
        readability_score = min(1.0, max(0.3, 1 - (word_count / 200)))  # Penalty for overly long text
        clarity_scores.append(readability_score * self.evaluation_criteria['clarity']['readability']['weight'])
        
        return sum(clarity_scores)

    def _evaluate_completeness(self, text: str, context: Dict[str, Any]) -> float:
        """
        Evaluate explanation completeness using SRTA framework.
        SRTAフレームワークを使用した説明完全性評価。

        Assesses coverage of What/Why/How/Who questions required
        for regulatory compliance.
        
        規制遵守に必要なWhat/Why/How/Who質問の
        カバレッジを評価します。
        """
        if not text:
            return 0.0
        
        text_lower = text.lower()
        completeness_scores = []
        
        # What coverage - decision description
        what_indicators = ['decision', 'result', 'output', 'recommendation', 'conclusion']
        what_coverage = 1.0 if any(indicator in text_lower for indicator in what_indicators) else 0.0
        completeness_scores.append(what_coverage * self.evaluation_criteria['completeness']['what_coverage']['weight'])
        
        # Why coverage - reasoning explanation (UNIQUE TO SRTA)
        why_indicators = ['because', 'due to', 'based on', 'reason', 'principle', 'justification']
        why_coverage = 1.0 if any(indicator in text_lower for indicator in why_indicators) else 0.0
        completeness_scores.append(why_coverage * self.evaluation_criteria['completeness']['why_coverage']['weight'])
        
        # How coverage - process description
        how_indicators = ['process', 'step', 'method', 'analysis', 'calculation', 'evaluation']
        how_coverage = 1.0 if any(indicator in text_lower for indicator in how_indicators) else 0.0
        completeness_scores.append(how_coverage * self.evaluation_criteria['completeness']['how_coverage']['weight'])
        
        # Who coverage - responsibility attribution (UNIQUE TO SRTA)
        who_indicators = ['stakeholder', 'responsible', 'team', 'officer', 'committee', 'authority']
        who_coverage = 1.0 if any(indicator in text_lower for indicator in who_indicators) else 0.0
        completeness_scores.append(who_coverage * self.evaluation_criteria['completeness']['who_coverage']['weight'])
        
        return sum(completeness_scores)

    def _evaluate_understandability(self, text: str, context: Dict[str, Any]) -> float:
        """Evaluate user understandability of explanation."""
        if not text:
            return 0.0
        
        understandability_scores = []
        
        # Length appropriateness
        text_length = len(text)
        min_length = self.evaluation_criteria['understandability']['explanation_length']['min']
        max_length = self.evaluation_criteria['understandability']['explanation_length']['max']
        
        if min_length <= text_length <= max_length:
            length_score = 1.0
        elif text_length < min_length:
            length_score = text_length / min_length
        else:
            length_score = max(0.3, max_length / text_length)
        
        understandability_scores.append(length_score * self.evaluation_criteria['understandability']['explanation_length']['weight'])
        
        # Structure clarity (presence of clear organization)
        structure_indicators = ['first', 'second', 'finally', 'therefore', 'however', 'additionally']
        structure_score = min(1.0, sum(1 for indicator in structure_indicators if indicator in text.lower()) / 3)
        understandability_scores.append(structure_score * self.evaluation_criteria['understandability']['structure_clarity']['weight'])
        
        # Context appropriateness (basic assessment)
        user_background = context.get('user_background', 'general')
        if user_background == 'technical':
            context_score = 0.8 + (0.2 if 'technical' in text.lower() or 'algorithm' in text.lower() else 0)
        elif user_background == 'general':
            context_score = 0.8 + (0.2 if len(text.split()) < 100 else 0)  # Prefer shorter explanations for general users
        else:
            context_score = 0.7
        
        understandability_scores.append(context_score * self.evaluation_criteria['understandability']['context_appropriateness']['weight'])
        
        return sum(understandability_scores)

    def _calculate_overall_score(self, clarity: float, completeness: float, 
                               understandability: float, confidence: float) -> float:
        """Calculate weighted overall quality score."""
        # Weight distribution
        weights = {
            'clarity': 0.25,
            'completeness': 0.35,        # Higher weight for regulatory compliance
            'understandability': 0.25,
            'confidence': 0.15
        }
        
        overall = (clarity * weights['clarity'] + 
                  completeness * weights['completeness'] +
                  understandability * weights['understandability'] +
                  confidence * weights['confidence'])
        
        return min(1.0, max(0.0, overall))

    def _determine_quality_level(self, overall_score: float) -> QualityLevel:
        """Determine quality level based on overall score."""
        if overall_score >= self.quality_thresholds[QualityLevel.EXCELLENT]:
            return QualityLevel.EXCELLENT
        elif overall_score >= self.quality_thresholds[QualityLevel.GOOD]:
            return QualityLevel.GOOD
        elif overall_score >= self.quality_thresholds[QualityLevel.FAIR]:
            return QualityLevel.FAIR
        else:
            return QualityLevel.POOR

    def _generate_improvement_suggestions(self, metrics: EvaluationMetrics, 
                                        context: Dict[str, Any]) -> List[str]:
        """Generate specific improvement suggestions based on evaluation."""
        suggestions = []
        
        # Clarity improvements
        if metrics.clarity < 0.7:
            suggestions.append("Simplify sentence structure and reduce technical jargon")
            suggestions.append("Break down complex concepts into smaller, digestible parts")
        
        # Completeness improvements
        if metrics.completeness < 0.8:
            suggestions.append("Ensure all four question types are addressed: What, Why, How, Who")
            if metrics.completeness < 0.5:
                suggestions.append("Add specific reasoning and stakeholder attribution")
        
        # Understandability improvements
        if metrics.understandability < 0.7:
            suggestions.append("Adjust explanation length and complexity for target audience")
            suggestions.append("Add structural elements like numbering or clear transitions")
        
        # Overall quality improvements
        if metrics.overall < 0.6:
            suggestions.append("Consider regenerating explanation with different style settings")
            suggestions.append("Review and enhance design principle justifications")
        
        return suggestions

    def _create_assessment_message(self, quality_level: QualityLevel, 
                                 overall_score: float, suggestion_count: int) -> str:
        """Create human-readable assessment message."""
        score_percentage = int(overall_score * 100)
        
        base_message = f"Explanation quality: {quality_level.value} ({score_percentage}%)"
        
        if suggestion_count > 0:
            base_message += f". {suggestion_count} improvement suggestions provided."
        else:
            base_message += ". No significant improvements needed."
        
        # Add regulatory compliance note
        if overall_score >= 0.8:
            base_message += " Meets regulatory transparency requirements."
        elif overall_score >= 0.6:
            base_message += " Partially meets transparency requirements - improvements recommended."
        else:
            base_message += " Does not meet regulatory transparency standards - significant improvements required."
        
        return base_message

    def get_evaluation_statistics(self) -> Dict[str, Any]:
        """Get evaluation layer performance statistics."""
        return {
            'total_evaluations': self.evaluation_count,
            'quality_thresholds': {level.value: threshold for level, threshold in self.quality_thresholds.items()},
            'evaluation_criteria_count': sum(len(criteria) for criteria in self.evaluation_criteria.values()),
            'supported_question_types': ['What', 'Why', 'How', 'Who'],
            'regulatory_compliance_enabled': True
        }

    def update_quality_thresholds(self, new_thresholds: Dict[QualityLevel, float]):
        """Update quality assessment thresholds."""
        self.quality_thresholds.update(new_thresholds)
        print(f"Quality thresholds updated for {len(new_thresholds)} levels")

    def export_evaluation_config(self) -> Dict[str, Any]:
        """Export current evaluation configuration."""
        return {
            'quality_thresholds': {level.value: threshold for level, threshold in self.quality_thresholds.items()},
            'evaluation_criteria': self.evaluation_criteria,
            'evaluation_count': self.evaluation_count,
            'export_timestamp': datetime.now().isoformat()
        }


# Demonstration and testing
if __name__ == "__main__":
    """
    Demonstration of Evaluation Layer capabilities.
    Evaluation Layer能力のデモンストレーション。
    """
    
    print("SRTA Evaluation Layer - Quality Assessment")
    print("SRTA評価レイヤー - 品質評価")
    print("=" * 50)
    
    # Initialize Evaluation Layer
    evaluation_layer = EvaluationLayer()
    
    # Test with sample explanations of varying quality
    test_explanations = [
        {
            'name': 'High Quality',
            'context': {
                'explanation_text': 'The system decided to approve the loan application because the applicant meets our fairness criteria with a credit score of 750 and stable income. This decision was made through a systematic analysis process involving data protection principles. The AI Ethics Committee and Data Protection Officer share responsibility for this recommendation. Confidence: 85%',
                'confidence': 0.85,
                'user_background': 'general'
            }
        },
        {
            'name': 'Medium Quality', 
            'context': {
                'explanation_text': 'Loan approved based on credit analysis. Score: 750. Good income. System confidence: 70%',
                'confidence': 0.70,
                'user_background': 'general'
            }
        },
        {
            'name': 'Low Quality',
            'context': {
                'explanation_text': 'Approved.',
                'confidence': 0.50,
                'user_background': 'general'
            }
        }
    ]
    
    print("Evaluating explanation quality...")
    print("説明品質を評価中...")
    
    for test in test_explanations:
        print(f"\nTesting: {test['name']}")
        print(f"テスト中: {test['name']}")
        
        result = evaluation_layer.evaluate_explanation(test['context'])
        
        print(f"Overall Score: {result.metrics.overall:.2f}")
        print(f"Quality Level: {result.quality_level.value}")
        print(f"Assessment: {result.assessment_message}")
        
        if result.improvement_suggestions:
            print(f"Suggestions ({len(result.improvement_suggestions)}):")
            for i, suggestion in enumerate(result.improvement_suggestions, 1):
                print(f"  {i}. {suggestion}")
        
        print(f"Processing Time: {result.processing_time:.1f}ms")
    
    # Display evaluation statistics
    stats = evaluation_layer.get_evaluation_statistics()
    print(f"\nEvaluation Statistics:")
    print(f"評価統計:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
