"""
SRTA Responsibility Tracker - Enhanced Version
Improved 4-dimension responsibility analysis with better calibration
"""

import time
import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ResponsibilityLevel(Enum):
    FULLY_TRACEABLE = "Fully Traceable"
    MOSTLY_TRACEABLE = "Mostly Traceable"
    PARTIALLY_TRACEABLE = "Partially Traceable"
    NOT_TRACEABLE = "Not Traceable"

@dataclass
class ResponsibilityMetrics:
    decision_traceability: float = 0.0
    data_lineage: float = 0.0
    actor_identification: float = 0.0
    process_transparency: float = 0.0
    overall: float = 0.0
    confidence_score: float = 0.0

@dataclass
class ResponsibilityResult:
    metrics: ResponsibilityMetrics
    level: ResponsibilityLevel
    traceable_components: List[str]
    missing_components: List[str]
    assessment_message: str
    processing_time: float
    detailed_analysis: Dict[str, Any]
    
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'metrics': {
                'decision_traceability': self.metrics.decision_traceability,
                'data_lineage': self.metrics.data_lineage,
                'actor_identification': self.metrics.actor_identification,
                'process_transparency': self.metrics.process_transparency,
                'overall': self.metrics.overall,
                'confidence_score': self.metrics.confidence_score
            },
            'level': self.level.value,
            'traceable_components': self.traceable_components,
            'missing_components': self.missing_components,
            'assessment_message': self.assessment_message,
            'processing_time': self.processing_time,
            'detailed_analysis': self.detailed_analysis
        }

class ResponsibilityTracker:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.responsibility_thresholds = self.config.get('responsibility_thresholds', {
            ResponsibilityLevel.FULLY_TRACEABLE: 0.85,
            ResponsibilityLevel.MOSTLY_TRACEABLE: 0.70,
            ResponsibilityLevel.PARTIALLY_TRACEABLE: 0.55,
            ResponsibilityLevel.NOT_TRACEABLE: 0.40
        })
        
        logger.info("SRTA Responsibility Tracker (Enhanced) initialized")
    
    def evaluate(self, context: Dict[str, Any]) -> ResponsibilityResult:
        start_time = time.time()
        
        try:
            text = context.get('explanation_text', '')
            
            decision_score = self._evaluate_decision_traceability(text, context)
            data_score = self._evaluate_data_lineage(text, context)
            actor_score = self._evaluate_actor_identification(text, context)
            process_score = self._evaluate_process_transparency(text, context)
            
            overall = (decision_score + data_score + actor_score + process_score) / 4
            confidence = self._calculate_confidence(text, context)
            
            metrics = ResponsibilityMetrics(
                decision_traceability=decision_score,
                data_lineage=data_score,
                actor_identification=actor_score,
                process_transparency=process_score,
                overall=overall,
                confidence_score=confidence
            )
            
            level = self._determine_responsibility_level(overall)
            traceable = self._identify_traceable_components(metrics)
            missing = self._identify_missing_components(metrics)
            message = self._generate_responsibility_message(level)
            
            detailed_analysis = {
                'decision_indicators': self._get_decision_indicators(text),
                'data_indicators': self._get_data_indicators(text),
                'actor_info': self._get_actor_info(context),
                'process_indicators': self._get_process_indicators(text)
            }
            
            return ResponsibilityResult(
                metrics=metrics,
                level=level,
                traceable_components=traceable,
                missing_components=missing,
                assessment_message=message,
                processing_time=time.time() - start_time,
                detailed_analysis=detailed_analysis
            )
            
        except Exception as e:
            logger.error(f"Responsibility evaluation failed: {str(e)}")
            raise ValueError(f"責任追跡評価中にエラーが発生しました: {str(e)}") from e
    
    def _evaluate_decision_traceability(self, text: str, context: Dict[str, Any]) -> float:
        base_score = 0.2
        text_lower = text.lower()
        
        # Decision indicators
        decision_words = ['classified', 'determined', 'decided', 'concluded', 'predicted']
        if any(word in text_lower for word in decision_words):
            base_score += 0.2
        
        # Confidence indicators
        confidence_words = ['confidence', 'probability', 'likely', 'certain', '%']
        if any(word in text_lower for word in confidence_words):
            base_score += 0.2
        
        # Context confidence
        if context.get('confidence'):
            base_score += 0.2
        
        # Reasoning chain
        reasoning_words = ['because', 'since', 'due to', 'based on', 'therefore']
        if any(word in text_lower for word in reasoning_words):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _evaluate_data_lineage(self, text: str, context: Dict[str, Any]) -> float:
        base_score = 0.1
        text_lower = text.lower()
        
        # Data source indicators
        data_words = ['dataset', 'training', 'data', 'input', 'model', 'learned']
        found_data = sum(1 for word in data_words if word in text_lower)
        base_score += min(found_data * 0.1, 0.3)
        
        # Processing indicators
        process_words = ['processed', 'analyzed', 'extracted', 'computed', 'trained']
        found_process = sum(1 for word in process_words if word in text_lower)
        base_score += min(found_process * 0.1, 0.25)
        
        # Technical specifications
        tech_words = ['neural', 'network', 'algorithm', 'resnet', 'cnn']
        if any(word in text_lower for word in tech_words):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _evaluate_actor_identification(self, text: str, context: Dict[str, Any]) -> float:
        base_score = 0.3
        
        # Context-based identification
        if context.get('actor_id'):
            base_score += 0.25
        if context.get('actor_type'):
            base_score += 0.15
        if context.get('responsible_entity'):
            base_score += 0.15
        
        # Text-based identification
        system_words = ['model', 'system', 'algorithm', 'ai', 'classifier']
        if any(word in text.lower() for word in system_words):
            base_score += 0.15
        
        return min(base_score, 1.0)
    
    def _evaluate_process_transparency(self, text: str, context: Dict[str, Any]) -> float:
        base_score = 0.2
        text_lower = text.lower()
        
        # Process methodology
        method_words = ['algorithm', 'method', 'process', 'procedure', 'approach']
        if any(word in text_lower for word in method_words):
            base_score += 0.2
        
        # Sequential indicators
        sequence_patterns = [r'\\d+\\.', r'first', r'then', r'next', r'finally']
        if any(re.search(pattern, text_lower) for pattern in sequence_patterns):
            base_score += 0.25
        
        # Technical detail
        tech_words = ['layer', 'filter', 'convolution', 'pooling', 'softmax']
        found_tech = sum(1 for word in tech_words if word in text_lower)
        base_score += min(found_tech * 0.05, 0.2)
        
        return min(base_score, 1.0)
    
    def _calculate_confidence(self, text: str, context: Dict[str, Any]) -> float:
        factors = []
        
        # Text length
        word_count = len(text.split())
        if word_count >= 20:
            factors.append(0.3)
        elif word_count >= 10:
            factors.append(0.2)
        else:
            factors.append(0.1)
        
        # Context richness
        context_score = len([v for v in context.values() if v]) / max(len(context), 1)
        factors.append(context_score * 0.3)
        
        # Structure presence
        has_structure = bool(re.search(r'\\d+\\.|\\bfirst\\b|\\bthen\\b', text.lower()))
        factors.append(0.4 if has_structure else 0.2)
        
        return min(sum(factors), 1.0)
    
    def _determine_responsibility_level(self, score: float) -> ResponsibilityLevel:
        for level in [ResponsibilityLevel.FULLY_TRACEABLE, ResponsibilityLevel.MOSTLY_TRACEABLE, 
                      ResponsibilityLevel.PARTIALLY_TRACEABLE]:
            if score >= self.responsibility_thresholds[level]:
                return level
        return ResponsibilityLevel.NOT_TRACEABLE
    
    def _identify_traceable_components(self, metrics: ResponsibilityMetrics) -> List[str]:
        traceable = []
        threshold = 0.6
        
        if metrics.decision_traceability >= threshold:
            traceable.append(f"意思決定プロセス ({metrics.decision_traceability:.1%})")
        if metrics.data_lineage >= threshold:
            traceable.append(f"データ系譜 ({metrics.data_lineage:.1%})")
        if metrics.actor_identification >= threshold:
            traceable.append(f"関与者特定 ({metrics.actor_identification:.1%})")
        if metrics.process_transparency >= threshold:
            traceable.append(f"プロセス透明性 ({metrics.process_transparency:.1%})")
        
        return traceable
    
    def _identify_missing_components(self, metrics: ResponsibilityMetrics) -> List[str]:
        missing = []
        threshold = 0.6
        
        if metrics.decision_traceability < threshold:
            missing.append("意思決定根拠の明示")
        if metrics.data_lineage < threshold:
            missing.append("データソース情報")
        if metrics.actor_identification < threshold:
            missing.append("責任者情報")
        if metrics.process_transparency < threshold:
            missing.append("処理プロセス詳細")
        
        return missing
    
    def _generate_responsibility_message(self, level: ResponsibilityLevel) -> str:
        messages = {
            ResponsibilityLevel.FULLY_TRACEABLE: "完全な責任追跡が可能で、監査要件を満たしています。",
            ResponsibilityLevel.MOSTLY_TRACEABLE: "概ね責任追跡が可能ですが、一部改善の余地があります。",
            ResponsibilityLevel.PARTIALLY_TRACEABLE: "部分的な責任追跡のみ可能で、重要な情報が不足しています。",
            ResponsibilityLevel.NOT_TRACEABLE: "責任追跡が困難で、透明性の大幅な改善が必要です。"
        }
        return messages[level]
    
    def _get_decision_indicators(self, text: str) -> List[str]:
        indicators = []
        decision_words = ['classified', 'determined', 'decided', 'concluded', 'predicted']
        for word in decision_words:
            if word in text.lower():
                indicators.append(word)
        return indicators
    
    def _get_data_indicators(self, text: str) -> List[str]:
        indicators = []
        data_words = ['dataset', 'training', 'model', 'input', 'features']
        for word in data_words:
            if word in text.lower():
                indicators.append(word)
        return indicators
    
    def _get_actor_info(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'actor_id': context.get('actor_id'),
            'actor_type': context.get('actor_type'),
            'responsible_entity': context.get('responsible_entity')
        }
    
    def _get_process_indicators(self, text: str) -> List[str]:
        indicators = []
        process_words = ['algorithm', 'method', 'process', 'layer', 'network']
        for word in process_words:
            if word in text.lower():
                indicators.append(word)
        return indicators

def main():
    print("SRTA Responsibility Tracker Enhanced - Test Suite")
    print("=" * 60)
    
    tracker = ResponsibilityTracker()
    
    test_cases = [
        {
            'name': 'Comprehensive Context',
            'explanation_text': """
The ResNet-50 model classified this input image as 'cat' with 94.2% confidence.
First, the convolutional layers extracted edge features from the input pixels.
Then, pooling layers identified triangular ear shapes characteristic of felines.
Finally, the classification head applied softmax to determine the most likely category.
This decision was based on training data from ImageNet containing 1.2M labeled images.
            """.strip(),
            'actor_id': 'resnet50_v2.1',
            'actor_type': 'neural_network',
            'responsible_entity': 'AI Research Lab',
            'confidence': 0.942
        },
        {
            'name': 'Minimal Context',
            'explanation_text': "It's a cat.",
            'confidence': 0.6
        },
        {
            'name': 'Technical Detail',
            'explanation_text': """
Classification performed using deep convolutional neural network architecture.
Multi-scale feature extraction through hierarchical pooling operations.
Backpropagation training on supervised dataset with cross-entropy loss.
Output probability distribution normalized via softmax activation function.
            """.strip(),
            'actor_type': 'ai_system'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n{'='*15} Test {i}: {test_case['name']} {'='*15}")
        
        context = {k: v for k, v in test_case.items() if k != 'name'}
        
        try:
            result = tracker.evaluate(context)
            
            print(f"Responsibility Analysis:")
            print(f"   Decision Traceability: {result.metrics.decision_traceability:.1%}")
            print(f"   Data Lineage: {result.metrics.data_lineage:.1%}")
            print(f"   Actor Identification: {result.metrics.actor_identification:.1%}")
            print(f"   Process Transparency: {result.metrics.process_transparency:.1%}")
            print(f"   Overall: {result.metrics.overall:.1%}")
            print(f"Responsibility Level: {result.level.value}")
            print(f"Confidence: {result.metrics.confidence_score:.1%}")
            print(f"Processing Time: {result.processing_time:.3f}s")
            
            if result.traceable_components:
                print(f"Traceable Components:")
                for component in result.traceable_components:
                    print(f"   ✓ {component}")
            
            if result.missing_components:
                print(f"Missing Components:")
                for component in result.missing_components:
                    print(f"   ✗ {component}")
            
            print(f"Assessment: {result.assessment_message}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print(f"\\n{'='*60}")
    print("Enhanced Responsibility Tracker testing complete!")

if __name__ == "__main__":
    main()
