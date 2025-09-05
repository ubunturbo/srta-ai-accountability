#!/usr/bin/env python3
"""
Enhanced Unified SRTA Evaluation System - Fixed Version
統合SRTA評価システム - 修正版
"""

import logging
import time
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

# 正しいクラス名でインポート
from evaluation_layer_enhanced_v2 import EvaluationLayer, EvaluationResult
from responsibility_tracker_enhanced import ResponsibilityTracker, ResponsibilityResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CorrelationInsights:
    pattern_classification: str
    correlation_strength: float
    gap_analysis: Dict[str, float]
    dimensional_balance: Dict[str, float]
    improvement_priority: List[str]
    statistical_confidence: float

@dataclass
class UnifiedEvaluationResult:
    unified_score: float
    responsibility_analysis: Dict[str, Any]
    quality_assessment: Dict[str, Any]
    correlation_insights: CorrelationInsights
    confidence_metrics: Dict[str, float]
    recommendations: List[str]
    overall_assessment: str
    processing_time: float

class EnhancedUnifiedSRTAEvaluationLayer:
    """統合SRTA評価システム - 修正版"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.weights = config.get('weights', {'responsibility': 0.6, 'quality': 0.4})
        
        # 正しいクラス名で初期化
        self.responsibility_tracker = ResponsibilityTracker()
        self.quality_evaluator = EvaluationLayer(config)
        
        logger.info("Enhanced Unified SRTA Evaluation System initialized")
    
    def comprehensive_evaluate(self, context: Dict[str, Any]) -> UnifiedEvaluationResult:
        """包括的な統合評価の実行"""
        start_time = time.time()
        
        try:
            # 責任追跡評価
            resp_result = self.responsibility_tracker.comprehensive_track(context)
            
            # 品質評価 
            qual_result = self.quality_evaluator.evaluate_explanation(
                context.get('explanation_text', ''), context
            )
            
            # 基本的な統合スコア計算
            unified_score = (resp_result.metrics.overall * self.weights['responsibility'] +
                           qual_result.metrics.overall * self.weights['quality'])
            
            # 簡単な相関分析
            correlation_insights = self._analyze_basic_correlations(resp_result, qual_result)
            
            # 推奨事項生成
            recommendations = self._generate_basic_recommendations(resp_result, qual_result)
            
            processing_time = time.time() - start_time
            
            return UnifiedEvaluationResult(
                unified_score=unified_score,
                responsibility_analysis={
                    'metrics': resp_result.metrics.__dict__,
                    'detailed_analysis': resp_result.detailed_analysis
                },
                quality_assessment={
                    'metrics': qual_result.metrics.__dict__
                },
                correlation_insights=correlation_insights,
                confidence_metrics={
                    'responsibility_confidence': resp_result.metrics.confidence_score,
                    'quality_confidence': qual_result.confidence_score,
                    'overall_confidence': (resp_result.metrics.confidence_score + 
                                         qual_result.confidence_score) / 2
                },
                recommendations=recommendations,
                overall_assessment=f"統合評価: {unified_score:.1%}",
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            raise
    
    def _analyze_basic_correlations(self, resp_result: ResponsibilityResult, 
                                   qual_result: EvaluationResult) -> CorrelationInsights:
        """基本的な相関分析"""
        
        gap = abs(resp_result.metrics.overall - qual_result.metrics.overall)
        correlation = 1.0 - gap
        
        # パターン分類
        if resp_result.metrics.overall >= 0.7 and qual_result.metrics.overall >= 0.7:
            pattern = "理想的統合状態"
        elif resp_result.metrics.overall >= 0.7 and qual_result.metrics.overall < 0.6:
            pattern = "責任明確・品質不足"
        elif resp_result.metrics.overall < 0.6 and qual_result.metrics.overall >= 0.7:
            pattern = "品質良好・責任不明"
        else:
            pattern = "バランス調整必要"
        
        return CorrelationInsights(
            pattern_classification=pattern,
            correlation_strength=correlation,
            gap_analysis={'responsibility_quality_gap': gap},
            dimensional_balance={'overall_balance': min(resp_result.metrics.overall, qual_result.metrics.overall)},
            improvement_priority=[],
            statistical_confidence=min(resp_result.metrics.confidence_score, qual_result.confidence_score)
        )
    
    def _generate_basic_recommendations(self, resp_result: ResponsibilityResult,
                                       qual_result: EvaluationResult) -> List[str]:
        """基本的な推奨事項生成"""
        recommendations = []
        
        if resp_result.metrics.overall < 0.6:
            recommendations.append("責任情報の詳細化が必要")
        if qual_result.metrics.overall < 0.6:
            recommendations.append("説明品質の向上が必要")
        if abs(resp_result.metrics.overall - qual_result.metrics.overall) > 0.3:
            recommendations.append("責任と品質のバランス調整が必要")
        
        return recommendations or ["現在の水準維持を推奨"]

def main():
    """テスト実行"""
    print("Enhanced Unified SRTA Evaluation System - Fixed Version Test")
    print("=" * 60)
    
    config = {
        'weights': {'responsibility': 0.6, 'quality': 0.4},
        'transparency_optimal_length': 30
    }
    
    try:
        evaluator = EnhancedUnifiedSRTAEvaluationLayer(config)
        
        test_context = {
            'explanation_text': 'ResNet-50ニューラルネットワークが画像を94.2%の信頼度で猫として分類。畳み込み層がエッジ特徴を抽出し、プーリング操作で三角形耳形状を特定。',
            'actor_id': 'resnet50_v2.1',
            'actor_type': 'neural_network',
            'responsible_entity': 'AI Research Lab',
            'confidence': 0.942
        }
        
        print("統合評価テスト実行中...")
        result = evaluator.comprehensive_evaluate(test_context)
        
        print(f"\n=== 評価結果 ===")
        print(f"統合スコア: {result.unified_score:.1%}")
        print(f"責任追跡: {result.responsibility_analysis['metrics']['overall']:.1%}")
        print(f"品質評価: {result.quality_assessment['metrics']['overall']:.1%}")
        print(f"相関パターン: {result.correlation_insights.pattern_classification}")
        print(f"処理時間: {result.processing_time:.3f}s")
        
        print(f"\n=== 推奨事項 ===")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"{i}. {rec}")
        
        print(f"\n総合評価: {result.overall_assessment}")
        print("\nテスト完了!")
        
    except Exception as e:
        print(f"エラー発生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
