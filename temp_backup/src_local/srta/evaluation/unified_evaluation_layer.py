"""
Unified SRTA Evaluation System - 既存プロジェクト統合版
責任追跡 + 品質評価の統合システム (既存アーキテクチャ適合)
"""

import time
import logging
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# 既存モジュールとの互換性
from .evaluation_layer_enhanced import EvaluationLayer, EvaluationResult
from .responsibility_tracker import ResponsibilityTracker, ResponsibilityResult

logger = logging.getLogger(__name__)

@dataclass
class UnifiedEvaluationResult:
    quality_assessment: Dict[str, Any]
    responsibility_analysis: Dict[str, Any]
    correlation_analysis: Dict[str, Any]
    unified_score: float
    recommendations: List[str]
    overall_assessment: str
    timestamp: str
    processing_time: float
    
    def __getitem__(self, key: str) -> Any:
        """辞書アクセス対応"""
        return getattr(self, key)
    
    def to_dict(self) -> Dict[str, Any]:
        """完全な辞書形式での結果取得"""
        return asdict(self)

class UnifiedSRTAEvaluationLayer:
    """SRTA責任追跡 + 品質評価統合システム (既存プロジェクト適合版)"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # 既存システム初期化
        self.quality_evaluator = EvaluationLayer(config)
        self.responsibility_tracker = ResponsibilityTracker(config)
        
        # 統合スコア重み設定
        self.weights = self.config.get('weights', {
            'responsibility': 0.6,  # 責任追跡の重要度
            'quality': 0.4          # 品質評価の重要度
        })
        
        logger.info("🎯 Unified SRTA Evaluation Layer (Project Integration Version) initialized")
    
    def comprehensive_evaluate(self, context: Dict[str, Any]) -> UnifiedEvaluationResult:
        """包括的評価の実行 (既存API互換)"""
        start_time = time.time()
        
        try:
            # 個別評価の実行
            quality_result = self.quality_evaluator.evaluate_explanation(context)
            responsibility_result = self.responsibility_tracker.evaluate(context)
            
            # 相関分析
            correlation_analysis = self._analyze_correlations(responsibility_result, quality_result)
            
            # 統合スコア計算
            unified_score = self._calculate_unified_score(responsibility_result, quality_result)
            
            # 統合推奨事項生成
            recommendations = self._generate_unified_recommendations(
                responsibility_result, quality_result, correlation_analysis
            )
            
            # 総合評価メッセージ
            overall_assessment = self._generate_overall_assessment(unified_score, correlation_analysis)
            
            return UnifiedEvaluationResult(
                quality_assessment=quality_result.to_dict(),
                responsibility_analysis=responsibility_result.to_dict(),
                correlation_analysis=correlation_analysis,
                unified_score=unified_score,
                recommendations=recommendations,
                overall_assessment=overall_assessment,
                timestamp=datetime.now().isoformat(),
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Unified evaluation failed: {str(e)}")
            raise
    
    def evaluate_explanation(self, context: Dict[str, Any]) -> UnifiedEvaluationResult:
        """既存API互換のためのエイリアス"""
        return self.comprehensive_evaluate(context)
    
    def _analyze_correlations(self, resp_result: ResponsibilityResult, qual_result: EvaluationResult) -> Dict[str, Any]:
        """責任追跡と品質評価の相関分析"""
        resp_overall = resp_result.metrics.overall
        qual_overall = qual_result.metrics.overall
        
        # 相関スコア計算
        correlation_score = 1 - abs(resp_overall - qual_overall)
        
        # パターン分析
        if resp_overall > 0.8 and qual_overall > 0.8:
            pattern = "高責任追跡・高品質"
            insight = "理想的な状態 - 透明性と品質の両方が優秀"
        elif resp_overall > 0.7 and qual_overall < 0.6:
            pattern = "高責任追跡・低品質"
            insight = "プロセスは透明だが説明品質に課題"
        elif resp_overall < 0.6 and qual_overall > 0.7:
            pattern = "低責任追跡・高品質"
            insight = "説明品質は良いが透明性に課題"
        else:
            pattern = "要改善"
            insight = "責任追跡と品質の両方に改善が必要"
        
        return {
            'correlation_score': correlation_score,
            'pattern': pattern,
            'insight': insight,
            'responsibility_score': resp_overall,
            'quality_score': qual_overall
        }
    
    def _calculate_unified_score(self, resp_result: ResponsibilityResult, qual_result: EvaluationResult) -> float:
        """統合スコアの計算"""
        resp_score = resp_result.metrics.overall
        qual_score = qual_result.metrics.overall
        
        unified = (resp_score * self.weights['responsibility'] + 
                  qual_score * self.weights['quality'])
        
        return round(unified, 3)
    
    def _generate_unified_recommendations(self, resp_result: ResponsibilityResult, 
                                        qual_result: EvaluationResult, 
                                        correlation: Dict[str, Any]) -> List[str]:
        """統合推奨事項の生成"""
        recommendations = []
        
        # 個別推奨事項の統合
        if resp_result.missing_components:
            recommendations.append(f"責任追跡改善: {', '.join(resp_result.missing_components)}")
        
        if qual_result.improvement_suggestions and qual_result.improvement_suggestions[0] != "優秀な品質です - 改善の必要はありません":
            recommendations.append(f"品質改善: {', '.join(qual_result.improvement_suggestions)}")
        
        # 相関に基づく推奨事項
        if correlation['pattern'] == "高責任追跡・低品質":
            recommendations.append("プロセス透明性を活かし、説明の構造化と具体例追加を重点実施")
        elif correlation['pattern'] == "低責任追跡・高品質":
            recommendations.append("説明品質の高さを維持しつつ、決定プロセスの明示を強化")
        elif correlation['correlation_score'] < 0.5:
            recommendations.append("責任追跡と品質評価の一貫性向上が必要")
        
        return recommendations or ["現状維持 - 優秀な状態を継続"]
    
    def _generate_overall_assessment(self, unified_score: float, correlation: Dict[str, Any]) -> str:
        """総合評価メッセージの生成"""
        if unified_score >= 0.9:
            level = "優秀"
        elif unified_score >= 0.75:
            level = "良好"
        elif unified_score >= 0.6:
            level = "普通"
        else:
            level = "要改善"
        
        return f"統合評価: {level} (スコア: {unified_score:.1%}) - {correlation['insight']}"

def main():
    """統合システムのテスト実行 (既存プロジェクト構造対応)"""
    print("🎯 Unified SRTA Evaluation System - Project Integration Test")
    print("=" * 60)
    
    # 統合評価システムの初期化
    config = {
        'weights': {'responsibility': 0.6, 'quality': 0.4},
        'quality_thresholds': {
            'EXCELLENT': 0.85,
            'GOOD': 0.70,
            'FAIR': 0.55,
            'POOR': 0.40
        }
    }
    
    unified_evaluator = UnifiedSRTAEvaluationLayer(config)
    
    # 既存プロジェクトでのテストケース
    test_context = {
        'explanation_text': """
This image classification decision was executed based on predefined quality criteria.

Decision Process:
1. Dataset: ImageNet pre-trained model usage
2. Processing: ResNet-50 architecture feature extraction  
3. Criteria: Confidence threshold 87% or higher for classification confirmation

For example, detected triangular ear shapes are characteristic indicators of felines.
Responsible: AI System Administrator (ID: SYS001)
        """.strip(),
        'actor_type': 'hybrid',
        'responsible_entity': 'AI System Administrator'
    }
    
    try:
        print("\n🔍 既存プロジェクト統合テスト実行中...")
        result = unified_evaluator.comprehensive_evaluate(test_context)
        
        print(f"\n📊 統合評価結果:")
        print(f"   統合スコア: {result.unified_score:.1%}")
        print(f"   相関パターン: {result.correlation_analysis['pattern']}")
        print(f"   処理時間: {result.processing_time:.3f}s")
        
        print(f"\n🔍 責任追跡分析:")
        resp = result.responsibility_analysis
        print(f"   レベル: {resp['level']}")
        print(f"   総合スコア: {resp['metrics']['overall']:.1%}")
        
        print(f"\n📈 品質評価:")
        qual = result.quality_assessment
        print(f"   レベル: {qual['quality_level']}")
        print(f"   総合スコア: {qual['metrics']['overall']:.1%}")
        
        print(f"\n💡 統合推奨事項:")
        for rec in result.recommendations:
            print(f"   • {rec}")
        
        print(f"\n📝 総合評価: {result.overall_assessment}")
        
        # 既存API互換性テスト
        print(f"\n🔧 既存API互換性テスト:")
        compat_result = unified_evaluator.evaluate_explanation(test_context)
        print(f"   evaluate_explanation() 互換性: ✅")
        print(f"   辞書アクセス result['unified_score']: {compat_result['unified_score']:.1%}")
        
        print(f"\n✅ 既存プロジェクト統合システム動作確認完了!")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
