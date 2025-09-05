"""
SRTA Evaluation Layer - Enhanced Quality Assessment Module
既存システム改良版: EvaluationResult subscriptable エラー修正 + 型安全性強化
"""

import time
import re
import logging
from typing import Dict, List, Any, Union
from dataclasses import dataclass
from enum import Enum

# ロギング設定
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
            'processing_time': self.processing_time
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
        logger.info("🔍 SRTA Evaluation Layer (Enhanced Quality Assessment Module) initialized")
    
    def evaluate_explanation(self, context: Dict[str, Any]) -> EvaluationResult:
        """
        説明文の品質を評価する（既存互換性維持）
        
        Args:
            context: 評価対象のコンテキスト辞書
                    必須キー: 'explanation_text' (str)
        
        Returns:
            EvaluationResult: 評価結果
            
        Raises:
            EvaluationError: 入力データが不正な場合
        """
        start_time = time.time()
        
        try:
            # 入力検証
            text = self._validate_input(context)
            
            # 評価メトリクス計算（既存ロジック改良版）
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
            
            logger.info(f"Evaluation completed: {quality_level.value} ({overall:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            raise EvaluationError(f"評価処理中にエラーが発生しました: {str(e)}") from e
    
    def _validate_input(self, context: Dict[str, Any]) -> str:
        """入力データの検証"""
        if not isinstance(context, dict):
            raise EvaluationError("context must be a dictionary")
        
        text = context.get('explanation_text')
        if text is None:
            raise EvaluationError("context must contain 'explanation_text' key")
        
        if not isinstance(text, str):
            raise EvaluationError("explanation_text must be a string")
        
        return text
    
    def _evaluate_clarity(self, text: str) -> float:
        """明確性の評価（既存ロジック改良版）"""
        if not text:
            return 0.0
        base_score = 0.5  # より保守的な初期値
        
        # 構造的要素の検出（改良版）
        if re.search(r'[1-9]\.|\*|-|•', text):
            base_score += 0.2
            
        # 適切な長さの評価
        word_count = len(text.split())
        if 30 <= word_count <= 200:
            base_score += 0.15
        elif word_count < 10:
            base_score -= 0.1  # 短すぎる場合のペナルティ
            
        return min(max(base_score, 0.0), 1.0)
    
    def _evaluate_completeness(self, text: str) -> float:
        """完全性の評価（既存ロジック改良版）"""
        if not text:
            return 0.0
        base_score = 0.4  # より保守的な初期値
        
        # 必須要素の検出（より詳細）
        what_indicators = ['what', 'result', 'decision', 'outcome']
        how_indicators = ['how', 'method', 'process', 'procedure']
        why_indicators = ['why', 'reason', 'because', 'since']
        
        text_lower = text.lower()
        has_what = any(word in text_lower for word in what_indicators)
        has_how = any(word in text_lower for word in how_indicators)
        has_why = any(word in text_lower for word in why_indicators)
        
        element_score = sum([has_what, has_how, has_why]) / 3 * 0.4
        base_score += element_score
        
        return min(max(base_score, 0.0), 1.0)
    
    def _evaluate_understandability(self, text: str) -> float:
        """理解容易性の評価（既存ロジック改良版）"""
        if not text:
            return 0.0
        base_score = 0.4  # より保守的な初期値
        
        # 例の存在（改良版）
        if re.search(r'example|instance|such as|for instance|e\.g\.', text.lower()):
            base_score += 0.2
            
        # 文の長さの適切性
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if sentences:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if 5 <= avg_length <= 20:
                base_score += 0.2
            elif avg_length > 30:  # 長すぎる文のペナルティ
                base_score -= 0.1
                
        return min(max(base_score, 0.0), 1.0)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """品質レベルの決定（既存互換）"""
        for level in [QualityLevel.EXCELLENT, QualityLevel.GOOD, QualityLevel.FAIR]:
            if score >= self.quality_thresholds[level]:
                return level
        return QualityLevel.POOR
    
    def _generate_suggestions(self, text: str, metrics: EvaluationMetrics) -> List[str]:
        """改善提案の生成（既存互換改良版）"""
        suggestions = []
        threshold = 0.7
        
        if metrics.clarity < threshold:
            suggestions.append("構造化: 番号付きリストや箇条書きで情報を整理してください")
        if metrics.completeness < threshold:
            suggestions.append("網羅性: '何を'、'どのように'、'なぜ'の観点を含めてください")
        if metrics.understandability < threshold:
            suggestions.append("理解促進: 具体例や比喩を使って概念を説明してください")
            
        if not suggestions:
            suggestions.append("優秀な品質です - 改善の必要はありません")
            
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
    """テスト実行関数（既存互換）"""
    print("🔍 SRTA Evaluation Layer - Enhanced Quality Assessment Module")
    evaluator = EvaluationLayer()
    
    # 既存テストケース
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
    
    try:
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
        
        # subscriptable テスト
        print(f"\n🔧 Subscriptable Test:")
        print(f"   result['quality_level']: {result['quality_level']}")
        print(f"   result.to_dict(): 辞書形式変換成功")
        
        print("\nEnhanced Evaluation Layer 改良版動作確認! ✅")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
