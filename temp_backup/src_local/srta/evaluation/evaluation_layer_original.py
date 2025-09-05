"""
SRTA Evaluation Layer - Quality Assessment Module (Enhanced Version)
"""

import time
import re
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class QualityLevel(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"

@dataclass
class EvaluationMetrics:
    clarity: float = 0.0
    completeness: float = 0.0
    understandability: float = 0.0
    overall: float = 0.0

@dataclass
class EvaluationResult:
    metrics: EvaluationMetrics
    quality_level: QualityLevel
    improvement_suggestions: List[str]
    assessment_message: str
    processing_time: float

class EvaluationLayer:
    def __init__(self):
        self.quality_thresholds = {
            QualityLevel.EXCELLENT: 0.9,
            QualityLevel.GOOD: 0.75,
            QualityLevel.FAIR: 0.6,
            QualityLevel.POOR: 0.4
        }
        print("🔍 SRTA Evaluation Layer (Enhanced Quality Assessment Module) initialized")
    
    def evaluate_explanation(self, context):
        start_time = time.time()
        
        # Enhanced evaluation
        text = context.get('explanation_text', '')
        
        # Calculate metrics
        clarity = self._evaluate_clarity(text)
        completeness = self._evaluate_completeness(text)
        understandability = self._evaluate_understandability(text)
        overall = (clarity + completeness + understandability) / 3
        
        metrics = EvaluationMetrics(
            clarity=clarity,
            completeness=completeness,
            understandability=understandability,
            overall=overall
        )
        
        quality_level = self._determine_quality_level(overall)
        suggestions = self._generate_suggestions(text, metrics)
        message = self._generate_message(quality_level)
        
        result = EvaluationResult(
            metrics=metrics,
            quality_level=quality_level,
            improvement_suggestions=suggestions,
            assessment_message=message,
            processing_time=time.time() - start_time
        )
        
        return result
    
    def _evaluate_clarity(self, text: str) -> float:
        if not text:
            return 0.0
        base_score = 0.7
        # Check for structured elements
        if re.search(r'[1-9]\.|\*|-', text):
            base_score += 0.2
        # Check length appropriateness
        word_count = len(text.split())
        if 30 <= word_count <= 200:
            base_score += 0.1
        return min(base_score, 1.0)
    
    def _evaluate_completeness(self, text: str) -> float:
        if not text:
            return 0.0
        base_score = 0.6
        # Check for essential elements
        has_what = any(word in text.lower() for word in ['what', 'result', 'decision'])
        has_how = any(word in text.lower() for word in ['how', 'method', 'process'])
        has_why = any(word in text.lower() for word in ['why', 'reason', 'because'])
        
        element_score = sum([has_what, has_how, has_why]) / 3 * 0.3
        base_score += element_score
        return min(base_score, 1.0)
    
    def _evaluate_understandability(self, text: str) -> float:
        if not text:
            return 0.0
        base_score = 0.6
        # Check for examples
        if re.search(r'example|instance|such as', text.lower()):
            base_score += 0.2
        # Check sentence length
        sentences = text.split('.')
        if sentences:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if 5 <= avg_length <= 20:
                base_score += 0.2
        return min(base_score, 1.0)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        if score >= self.quality_thresholds[QualityLevel.EXCELLENT]:
            return QualityLevel.EXCELLENT
        elif score >= self.quality_thresholds[QualityLevel.GOOD]:
            return QualityLevel.GOOD
        elif score >= self.quality_thresholds[QualityLevel.FAIR]:
            return QualityLevel.FAIR
        else:
            return QualityLevel.POOR
    
    def _generate_suggestions(self, text: str, metrics: EvaluationMetrics) -> List[str]:
        suggestions = []
        if metrics.clarity < 0.8:
            suggestions.append("Add structure with numbered points or bullet lists")
        if metrics.completeness < 0.8:
            suggestions.append("Include more details about the reasoning process")
        if metrics.understandability < 0.8:
            suggestions.append("Add concrete examples to illustrate concepts")
        if not suggestions:
            suggestions.append("Excellent quality - no improvements needed")
        return suggestions
    
    def _generate_message(self, quality_level: QualityLevel) -> str:
        messages = {
            QualityLevel.EXCELLENT: "Outstanding explanation quality with comprehensive coverage and clarity.",
            QualityLevel.GOOD: "Good quality explanation that effectively communicates the key information.",
            QualityLevel.FAIR: "Acceptable explanation with room for improvement in clarity and detail.",
            QualityLevel.POOR: "Explanation needs significant improvement to meet quality standards."
        }
        return messages[quality_level]

def main():
    print("🔍 SRTA Evaluation Layer - Enhanced Quality Assessment Module")
    evaluator = EvaluationLayer()
    
    # Test with sample explanation
    test_context = {
        'explanation_text': """
This image is classified as 'cat' with 87% confidence.

Classification reasoning:
1. Shape pattern analysis detected animal features
2. Edge detection identified ear shapes
3. Texture analysis confirmed fur patterns

For example, the triangular ear shapes are characteristic of felines.
This automated analysis provides reliable classification results.
        """.strip()
    }
    
    result = evaluator.evaluate_explanation(test_context)
    
    print(f"\n📊 Quality Assessment Results:")
    print(f"   Clarity: {result.metrics.clarity:.1%}")
    print(f"   Completeness: {result.metrics.completeness:.1%}")
    print(f"   Understandability: {result.metrics.understandability:.1%}")
    print(f"   Overall: {result.metrics.overall:.1%}")
    print(f"🏆 Quality Level: {result.quality_level.value}")
    print(f"⏱️ Processing Time: {result.processing_time:.3f}s")
    print(f"\n💡 Suggestions: {', '.join(result.improvement_suggestions)}")
    print(f"\n🔍 Assessment: {result.assessment_message}")
    print("\nEnhanced Evaluation Layer MVP working! ✅")

if __name__ == "__main__":
    main()
