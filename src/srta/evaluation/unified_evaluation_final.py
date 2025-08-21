#!/usr/bin/env python3
"""
Enhanced Unified SRTA Evaluation System - Final Working Version
統合SRTA評価システム - 最終動作版
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
    """統合SRTA評価システム - 最終版"""
    
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
            # 正しいメソッド名で評価実行
            resp_result = self.responsibility_tracker.evaluate(context)
            qual_result = self.quality_evaluator.evaluate_explanation(context)
            
            # 統合スコア計算
            unified_score = (resp_result.metrics.overall * self.weights['responsibility'] +
                           qual_result.metrics.overall * self.weights['quality'])
            
            # 拡張相関分析
            correlation_insights = self._analyze_enhanced_correlations(resp_result, qual_result)
            
            # 推奨事項生成
            recommendations = self._generate_enhanced_recommendations(resp_result, qual_result, correlation_insights)
            
            # 信頼度メトリクス
            confidence_metrics = self._calculate_unified_confidence(resp_result, qual_result, correlation_insights)
            
            # 総合評価
            overall_assessment = self._generate_enhanced_overall_assessment(unified_score, correlation_insights, confidence_metrics)
            
            processing_time = time.time() - start_time
            
            return UnifiedEvaluationResult(
                unified_score=unified_score,
                responsibility_analysis={
                    'metrics': resp_result.metrics.__dict__,
                    'overall': resp_result.metrics.overall,
                    'detailed_analysis': resp_result.detailed_analysis
                },
                quality_assessment={
                    'metrics': qual_result.metrics.__dict__,
                    'overall': qual_result.metrics.overall
                },
                correlation_insights=correlation_insights,
                confidence_metrics=confidence_metrics,
                recommendations=recommendations,
                overall_assessment=overall_assessment,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            raise
    
    def _analyze_enhanced_correlations(self, resp_result: ResponsibilityResult, 
                                     qual_result: EvaluationResult) -> CorrelationInsights:
        """拡張相関分析の実行"""
        
        # 20次元クロス相関マトリックス
        resp_scores = resp_result.metrics.__dict__
        qual_scores = qual_result.metrics.__dict__
        
        # クロス相関計算
        correlation_matrix = {}
        for resp_dim, resp_val in resp_scores.items():
            for qual_dim, qual_val in qual_scores.items():
                key = f"{resp_dim}_{qual_dim}"
                correlation_matrix[key] = self._calculate_correlation(resp_val, qual_val)
        
        # 全体相関強度
        overall_corr = sum(correlation_matrix.values()) / len(correlation_matrix)
        
        # ギャップ分析
        gap_analysis = {
            'responsibility_quality_gap': abs(resp_result.metrics.overall - qual_result.metrics.overall),
            'consistency_gap': self._calculate_consistency_gap(resp_scores, qual_scores),
            'balance_score': min(resp_result.metrics.overall, qual_result.metrics.overall) / 
                           max(resp_result.metrics.overall, qual_result.metrics.overall, 0.001)
        }
        
        # 次元バランス分析
        dimensional_balance = self._calculate_dimensional_balance(resp_scores, qual_scores)
        
        # パターン分類
        pattern = self._classify_correlation_pattern(resp_result.metrics.overall, 
                                                   qual_result.metrics.overall, overall_corr)
        
        # 改善優先度計算
        improvement_priority = self._calculate_improvement_priority(resp_result, qual_result, gap_analysis)
        
        # 統計的信頼度
        confidence_factors = [
            resp_result.metrics.confidence_score,
            qual_result.confidence_score,
            overall_corr,
            gap_analysis['balance_score'],
            1 - gap_analysis['responsibility_quality_gap']
        ]
        statistical_confidence = sum(confidence_factors) / len(confidence_factors)
        
        return CorrelationInsights(
            pattern_classification=pattern,
            correlation_strength=overall_corr,
            gap_analysis=gap_analysis,
            dimensional_balance=dimensional_balance,
            improvement_priority=improvement_priority,
            statistical_confidence=statistical_confidence
        )
    
    def _calculate_correlation(self, val1: float, val2: float) -> float:
        """シンプル相関計算"""
        return 1.0 - abs(val1 - val2)
    
    def _calculate_consistency_gap(self, scores1: Dict[str, float], scores2: Dict[str, float]) -> float:
        """一貫性ギャップ計算"""
        gaps = []
        for key in scores1.keys():
            if key in scores2:
                gaps.append(abs(scores1[key] - scores2[key]))
        return sum(gaps) / len(gaps) if gaps else 0.0
    
    def _calculate_dimensional_balance(self, resp_scores: Dict[str, float], qual_scores: Dict[str, float]) -> Dict[str, float]:
        """次元バランスメトリクス計算"""
        resp_variance = self._calculate_variance(list(resp_scores.values()))
        qual_variance = self._calculate_variance(list(qual_scores.values()))
        
        return {
            'responsibility_balance': 1.0 - resp_variance,
            'quality_balance': 1.0 - qual_variance,
            'overall_balance': 1.0 - ((resp_variance + qual_variance) / 2)
        }
    
    def _calculate_variance(self, values: List[float]) -> float:
        """分散計算"""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _classify_correlation_pattern(self, resp_score: float, qual_score: float, correlation: float) -> str:
        """相関パターン分類"""
        if resp_score >= 0.7 and qual_score >= 0.7:
            return "理想的統合状態"
        elif resp_score >= 0.7 and qual_score < 0.6:
            return "責任明確・品質不足"
        elif resp_score < 0.6 and qual_score >= 0.7:
            return "品質良好・責任不明"
        elif correlation < 0.5:
            return "非同期改善"
        else:
            return "バランス調整必要"
    
    def _calculate_improvement_priority(self, resp_result: ResponsibilityResult, qual_result: EvaluationResult, gap_analysis: Dict[str, float]) -> List[str]:
        """改善優先度計算"""
        dimensions = {
            'decision_traceability': resp_result.metrics.decision_traceability,
            'data_lineage': resp_result.metrics.data_lineage,
            'actor_identification': resp_result.metrics.actor_identification,
            'process_transparency': resp_result.metrics.process_transparency,
            'clarity': qual_result.metrics.clarity,
            'completeness': qual_result.metrics.completeness,
            'understandability': qual_result.metrics.understandability
        }
        
        sorted_dims = sorted(dimensions.items(), key=lambda x: x[1])
        return [dim for dim, score in sorted_dims if score < 0.7]
    
    def _generate_enhanced_recommendations(self, resp_result: ResponsibilityResult, qual_result: EvaluationResult, insights: CorrelationInsights) -> List[str]:
        """拡張推奨事項生成"""
        recommendations = []
        
        # パターン別推奨事項
        if insights.pattern_classification == "責任明確・品質不足":
            recommendations.append("責任追跡の強みを活かして説明品質向上: 明確な責任情報を基により詳細で構造化された説明を作成")
        elif insights.pattern_classification == "品質良好・責任不明":
            recommendations.append("説明品質の高さを維持しつつ責任情報強化: 決定プロセスと関与者情報の明示を追加")
        elif insights.pattern_classification == "非同期改善":
            recommendations.append("統合性向上: 責任追跡と品質評価の一貫性を高める統一的アプローチを採用")
        
        # ギャップベース推奨事項
        if insights.gap_analysis['responsibility_quality_gap'] > 0.3:
            recommendations.append("評価軸バランス調整: 責任追跡と品質評価の水準差を縮小する集中的改善")
        
        # 個別コンポーネント推奨事項
        if resp_result.metrics.decision_traceability < 0.6:
            recommendations.append("意思決定追跡強化: 判断根拠と決定プロセスの明示を重点改善")
        if qual_result.metrics.clarity < 0.6:
            recommendations.append("明確性向上: 構造化と論理的順序による理解容易性の改善")
        
        # 信頼度ベース推奨事項
        if insights.statistical_confidence < 0.6:
            recommendations.append("評価信頼性向上: より詳細な文脈情報と構造化された説明の提供")
        
        return recommendations or ["統合評価良好: 現在の水準維持を推奨"]
    
    def _calculate_unified_confidence(self, resp_result: ResponsibilityResult, qual_result: EvaluationResult, insights: CorrelationInsights) -> Dict[str, float]:
        """統合信頼度計算"""
        return {
            'responsibility_confidence': resp_result.metrics.confidence_score,
            'quality_confidence': qual_result.confidence_score,
            'correlation_confidence': insights.statistical_confidence,
            'overall_confidence': (resp_result.metrics.confidence_score +
                                 qual_result.confidence_score + 
                                 insights.statistical_confidence) / 3,
            'assessment_reliability': min(insights.statistical_confidence, insights.correlation_strength)
        }
    
    def _generate_enhanced_overall_assessment(self, unified_score: float, insights: CorrelationInsights, confidence: Dict[str, float]) -> str:
        """包括的総合評価生成"""
        # スコアベースレベル
        if unified_score >= 0.9:
            level = "優秀"
        elif unified_score >= 0.75:
            level = "良好"
        elif unified_score >= 0.6:
            level = "普通"
        else:
            level = "要改善"
        
        # 信頼度修飾子
        if confidence['overall_confidence'] >= 0.8:
            confidence_qualifier = "高信頼度"
        elif confidence['overall_confidence'] >= 0.6:
            confidence_qualifier = "中信頼度"
        else:
            confidence_qualifier = "低信頼度"
        
        return (f"統合評価: {level} (スコア: {unified_score:.1%}, {confidence_qualifier}) "
                f"- パターン: {insights.pattern_classification}, "
                f"相関: {insights.correlation_strength:.1%}")

def main():
    """テスト実行"""
    print("Enhanced Unified SRTA Evaluation System - Final Test Suite")
    print("=" * 70)
    
    config = {
        'weights': {'responsibility': 0.6, 'quality': 0.4},
        'transparency_optimal_length': 30
    }
    
    unified_evaluator = EnhancedUnifiedSRTAEvaluationLayer(config)
    
    test_cases = [
        {
            'name': '高品質・高責任テスト',
            'explanation_text': 'ResNet-50ニューラルネットワークが画像を94.2%の信頼度で猫として分類しました。まず畳み込み層が入力ピクセルからエッジ特徴を抽出し、次にプーリング操作で三角形の耳形状を特定しました。最終的に分類ヘッドがsoftmaxを適用して最も可能性の高いカテゴリを決定しました。',
            'actor_id': 'resnet50_v2.1',
            'actor_type': 'neural_network',
            'responsible_entity': 'AI Research Lab',
            'confidence': 0.942
        },
        {
            'name': '不均衡テスト（品質良好・責任不明）',
            'explanation_text': '画像には特徴的な特徴を持つ家猫が写っています。まず三角形の耳が猫科の特徴を示し、次にひげと顔構造が猫の識別を確認し、最後に毛の質感と体の比率がこの分類を支持しています。',
            'confidence': 0.85
        },
        {
            'name': '不均衡テスト（品質不足・責任明確）',
            'explanation_text': '訓練データに基づいて猫として分類されました。',
            'actor_id': 'classification_system_v1',
            'actor_type': 'ml_model',
            'responsible_entity': 'ML Engineering Team',
            'confidence': 0.78
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} テスト {i}: {test_case['name']} {'='*20}")
        context = {k: v for k, v in test_case.items() if k != 'name'}
        
        try:
            result = unified_evaluator.comprehensive_evaluate(context)
            
            print("統合評価結果:")
            print(f"   統合スコア: {result.unified_score:.1%}")
            print(f"   相関パターン: {result.correlation_insights.pattern_classification}")
            print(f"   相関強度: {result.correlation_insights.correlation_strength:.1%}")
            print(f"   統計的信頼度: {result.correlation_insights.statistical_confidence:.1%}")
            print(f"   処理時間: {result.processing_time:.3f}s")
            
            print("\n詳細分析:")
            print(f"   責任追跡: {result.responsibility_analysis['overall']:.1%}")
            print(f"   品質評価: {result.quality_assessment['overall']:.1%}")
            print(f"   評価信頼度: {result.confidence_metrics['overall_confidence']:.1%}")
            
            print("\n統合推奨事項:")
            for rec in result.recommendations:
                print(f"   • {rec}")
            
            print(f"\n総合評価: {result.overall_assessment}")
            
        except Exception as e:
            print(f"エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*70}")
    print("Enhanced Unified SRTA Evaluation System testing complete!")

if __name__ == "__main__":
    main()
