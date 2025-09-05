"""
SRTA Evaluation Layer - Enhanced Quality Assessment Module (Refined)
"""

import time
import re
import logging
from typing import Dict, List, Any, Union, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    confidence_score: float = 0.0  # New: evaluation confidence
    
    def __getitem__(self, key: str) -> Any:
        """EvaluationResult object subscriptable エラー対応"""
        return getattr(self, key)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式での結果取得"""
        return {
            'metrics': {
                'clarity': self.metrics.clarity,
                'completeness': self.metrics.completeness,
                'understandability': self.metrics.understandability,
                'overall': self.metrics.overall
            },
            'quality_level': self.quality_level.value,
            'improvement_suggestions': self.improvement_suggestions,
            'assessment_message': self.assessment_message,
            'processing_time': self.processing_time,
            'confidence_score': self.confidence_score
        }

class EvaluationError(Exception):
    """評価処理専用の例外クラス"""
    pass

class EvaluationLayer:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.quality_thresholds = self.config.get('quality_thresholds', {
            QualityLevel.EXCELLENT: 0.9,
            QualityLevel.GOOD: 0.75,
            QualityLevel.FAIR: 0.6,
            QualityLevel.POOR: 0.4
        })
        
        # Refined scoring parameters
        self.transparency_optimal_length = self.config.get('transparency_optimal_length', 25)
        self.clarity_indicators = self.config.get('clarity_indicators', [
            r'\\d+\\.', r'first', r'then', r'next', r'finally', r'because', r'since', r'therefore'
        ])
        
        logger.info("SRTA Evaluation Layer (Enhanced v2) initialized")
    
    def evaluate_explanation(self, context: Dict[str, Any]) -> EvaluationResult:
        """説明文の品質を評価する（改良版）"""
        start_time = time.time()
        
        try:
            text = self._validate_input(context)
            
            # Refined evaluation metrics
            clarity = self._evaluate_clarity_v2(text)
            completeness = self._evaluate_completeness_v2(text, context)
            understandability = self._evaluate_understandability_v2(text)
            overall = (clarity + completeness + understandability) / 3
            
            # Calculate confidence in evaluation
            confidence = self._calculate_confidence(text, context)
            
            metrics = EvaluationMetrics(
                clarity=clarity,
                completeness=completeness,
                understandability=understandability,
                overall=overall
            )
            
            quality_level = self._determine_quality_level(overall)
            suggestions = self._generate_suggestions_v2(text, metrics, context)
            message = self._generate_message(quality_level)
            
            result = EvaluationResult(
                metrics=metrics,
                quality_level=quality_level,
                improvement_suggestions=suggestions,
                assessment_message=message,
                processing_time=time.time() - start_time,
                confidence_score=confidence
            )
            
            logger.info(f"Evaluation completed: {quality_level.value} ({overall:.2f}, confidence: {confidence:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            raise EvaluationError(f"評価処理中にエラーが発生しました: {str(e)}") from e
    
    def _validate_input(self, context: Dict[str, Any]) -> str:
        """入力データの検証（強化版）"""
        if not isinstance(context, dict):
            raise EvaluationError("context must be a dictionary")
        
        text = context.get('explanation_text')
        if text is None:
            raise EvaluationError("context must contain 'explanation_text' key")
        
        if not isinstance(text, str):
            raise EvaluationError("explanation_text must be a string")
        
        if len(text.strip()) == 0:
            logger.warning("Empty explanation text provided")
            
        return text.strip()
    
    def _evaluate_clarity_v2(self, text: str) -> float:
        """明確性の評価（改良版）"""
        if not text:
            return 0.0
        
        base_score = 0.4
        
        # Structural indicators
        structure_score = 0.0
        for pattern in self.clarity_indicators:
            if re.search(pattern, text.lower()):
                structure_score += 0.1
        structure_score = min(structure_score, 0.3)
        
        # Length appropriateness (more nuanced)
        word_count = len(text.split())
        if 10 <= word_count <= 100:
            length_score = 0.2
        elif 5 <= word_count < 10 or 100 < word_count <= 200:
            length_score = 0.1
        else:
            length_score = 0.0
        
        # Sentence complexity
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            complexity_score = 0.1 if 5 <= avg_sentence_length <= 20 else 0.0
        else:
            complexity_score = 0.0
        
        return min(base_score + structure_score + length_score + complexity_score, 1.0)
    
    def _evaluate_completeness_v2(self, text: str, context: Dict[str, Any]) -> float:
        """完全性の評価（改良版）"""
        if not text:
            return 0.0
        
        base_score = 0.3
        text_lower = text.lower()
        
        # Enhanced completeness indicators
        what_indicators = ['what', 'result', 'decision', 'outcome', 'finding', 'classified', 'detected']
        how_indicators = ['how', 'method', 'process', 'algorithm', 'analysis', 'using', 'through']
        why_indicators = ['why', 'reason', 'because', 'since', 'due to', 'based on']
        
        has_what = any(word in text_lower for word in what_indicators)
        has_how = any(word in text_lower for word in how_indicators)
        has_why = any(word in text_lower for word in why_indicators)
        
        element_score = sum([has_what, has_how, has_why]) / 3 * 0.4
        
        # Context utilization
        context_score = 0.0
        if context.get('confidence') and 'confidence' in text_lower:
            context_score += 0.1
        if context.get('actor_id') and any(term in text_lower for term in ['model', 'system', 'algorithm']):
            context_score += 0.1
        
        # Detail level
        detail_score = min(len(text.split()) / 50.0, 0.2)
        
        return min(base_score + element_score + context_score + detail_score, 1.0)
    
    def _evaluate_understandability_v2(self, text: str) -> float:
        """理解容易性の評価（改良版）"""
        if not text:
            return 0.0
        
        base_score = 0.3
        
        # Examples and illustrations
        example_patterns = [
            r'example|instance|such as|for instance|e\\.g\\.',
            r'like|including|specifically|namely',
            r'consider|imagine|suppose'
        ]
        has_examples = any(re.search(pattern, text.lower()) for pattern in example_patterns)
        example_score = 0.2 if has_examples else 0.0
        
        # Technical term density
        technical_terms = re.findall(r'\\b[A-Z]{2,}\\b|\\b\\w*[Aa]lgorithm\\w*\\b|\\b\\w*[Mm]odel\\w*\\b', text)
        term_density = len(technical_terms) / max(len(text.split()), 1)
        if term_density > 0.3:  # Too technical
            technical_penalty = -0.1
        elif 0.1 <= term_density <= 0.3:  # Appropriate technical level
            technical_penalty = 0.1
        else:  # Too simple or no technical terms
            technical_penalty = 0.0
        
        # Readability (simple heuristic)
        avg_word_length = sum(len(word) for word in text.split()) / max(len(text.split()), 1)
        readability_score = 0.2 if 3 <= avg_word_length <= 6 else 0.1
        
        return min(max(base_score + example_score + technical_penalty + readability_score, 0.0), 1.0)
    
    def _calculate_confidence(self, text: str, context: Dict[str, Any]) -> float:
        """評価の信頼度を計算"""
        confidence_factors = []
        
        # Text length factor
        word_count = len(text.split())
        if word_count >= 10:
            confidence_factors.append(0.3)
        elif word_count >= 5:
            confidence_factors.append(0.2)
        else:
            confidence_factors.append(0.1)
        
        # Context richness
        context_richness = len([v for v in context.values() if v is not None]) / max(len(context), 1)
        confidence_factors.append(context_richness * 0.3)
        
        # Text structure
        has_structure = bool(re.search(r'\\d+\\.|\\*|-|because|since|therefore', text.lower()))
        confidence_factors.append(0.4 if has_structure else 0.2)
        
        return min(sum(confidence_factors), 1.0)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """品質レベルの決定（既存互換）"""
        for level in [QualityLevel.EXCELLENT, QualityLevel.GOOD, QualityLevel.FAIR]:
            if score >= self.quality_thresholds[level]:
                return level
        return QualityLevel.POOR
    
    def _generate_suggestions_v2(self, text: str, metrics: EvaluationMetrics, context: Dict[str, Any]) -> List[str]:
        """改善提案の生成（改良版）"""
        suggestions = []
        
        if metrics.clarity < 0.6:
            suggestions.append("構造改善: 「第一に」「次に」「なぜなら」などの接続詞で論理構造を明確化")
        
        if metrics.completeness < 0.6:
            if not any(word in text.lower() for word in ['what', 'result', 'decision']):
                suggestions.append("内容拡充: 「何が」決定されたかを明示")
            if not any(word in text.lower() for word in ['how', 'method', 'process']):
                suggestions.append("手法説明: 「どのように」判断したかのプロセスを追加")
            if not any(word in text.lower() for word in ['why', 'because', 'reason']):
                suggestions.append("根拠提示: 「なぜ」その結論に至ったかの理由を説明")
        
        if metrics.understandability < 0.6:
            if not re.search(r'example|instance|such as', text.lower()):
                suggestions.append("具体化: 具体例や比喩を用いて概念を説明")
            
            # Technical density check
            technical_terms = re.findall(r'\\b[A-Z]{2,}\\b|\\b\\w*[Aa]lgorithm\\w*\\b', text)
            if len(technical_terms) / max(len(text.split()), 1) > 0.3:
                suggestions.append("簡素化: 専門用語を減らし、一般的な表現に置き換え")
        
        if not suggestions:
            suggestions.append("高品質: 現在の説明品質は良好です")
        
        return suggestions
    
    def _generate_message(self, quality_level: QualityLevel) -> str:
        """評価メッセージの生成（既存互換）"""
        messages = {
            QualityLevel.EXCELLENT: "Outstanding explanation quality with comprehensive coverage and clarity.",
            QualityLevel.GOOD: "Good quality explanation that effectively communicates the key information.",
            QualityLevel.FAIR: "Acceptable explanation with room for improvement in clarity and detail.",
            QualityLevel.POOR: "Explanation needs significant improvement to meet quality standards."
        }
        return messages[quality_level]

def main():
    """テスト実行関数（改良版）"""
    print("SRTA Evaluation Layer - Enhanced v2 Test")
    
    evaluator = EvaluationLayer({
        'transparency_optimal_length': 30,
        'quality_thresholds': {
            QualityLevel.EXCELLENT: 0.85,
            QualityLevel.GOOD: 0.70,
            QualityLevel.FAIR: 0.55,
            QualityLevel.POOR: 0.40
        }
    })
    
    test_cases = [
        {
            'name': 'Technical Explanation',
            'explanation_text': """
The CNN model classified this image as 'cat' with 87% confidence through multi-stage analysis.
First, edge detection identified triangular ear shapes characteristic of felines.
Then, texture analysis confirmed fur patterns typical of domestic cats.
Finally, facial feature recognition detected whiskers and nose structure.
For example, the triangular ear geometry matches the learned cat feature templates.
            """.strip(),
            'confidence': 0.87,
            'actor_id': 'cnn_model_v2.1'
        },
        {
            'name': 'Simple Explanation',
            'explanation_text': "It's a cat because it has ears and fur.",
            'confidence': 0.60
        },
        {
            'name': 'Detailed Scientific',
            'explanation_text': """
The convolutional neural network processed the input image using ResNet-50 architecture.
Feature extraction occurred through multiple pooling layers analyzing pixel intensities.
The classification head applied softmax activation to probability distributions.
Confidence metrics indicated 94.2% likelihood of feline classification based on learned parameters.
            """.strip(),
            'confidence': 0.942,
            'model_type': 'ResNet-50'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n{'='*20} Test {i}: {test_case['name']} {'='*20}")
        
        try:
            result = evaluator.evaluate_explanation({
                'explanation_text': test_case['explanation_text'],
                **{k: v for k, v in test_case.items() if k != 'name' and k != 'explanation_text'}
            })
            
            print(f"Quality Assessment Results:")
            print(f"   Clarity: {result.metrics.clarity:.1%}")
            print(f"   Completeness: {result.metrics.completeness:.1%}")
            print(f"   Understandability: {result.metrics.understandability:.1%}")
            print(f"   Overall: {result.metrics.overall:.1%}")
            print(f"Quality Level: {result.quality_level.value}")
            print(f"Confidence: {result.confidence_score:.1%}")
            print(f"Processing Time: {result.processing_time:.3f}s")
            print(f"Suggestions:")
            for suggestion in result.improvement_suggestions:
                print(f"   • {suggestion}")
            print(f"Assessment: {result.assessment_message}")
            
            # Test subscriptable access
            print(f"Subscriptable test: {result['quality_level']}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print(f"\\nEnhanced Evaluation Layer v2 testing complete!")

if __name__ == "__main__":
    main()
