import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import src.srta.evaluation.evaluation_layer_enhanced as eval_enhanced
import src.srta.evaluation.responsibility_tracker as resp_tracker

import time
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

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

class UnifiedSRTAEvaluationLayer:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.quality_evaluator = eval_enhanced.EvaluationLayer(config)
        self.responsibility_tracker = resp_tracker.ResponsibilityTracker(config)
        self.weights = self.config.get('weights', {'responsibility': 0.6, 'quality': 0.4})
        print("統合SRTA評価レイヤー初期化完了")
    
    def comprehensive_evaluate(self, context: Dict[str, Any]) -> UnifiedEvaluationResult:
        start_time = time.time()
        
        quality_result = self.quality_evaluator.evaluate_explanation(context)
        responsibility_result = self.responsibility_tracker.evaluate(context)
        
        resp_overall = responsibility_result.metrics.overall
        qual_overall = quality_result.metrics.overall
        correlation_score = 1 - abs(resp_overall - qual_overall)
        
        if resp_overall > 0.8 and qual_overall > 0.8:
            pattern = "高責任追跡・高品質"
            insight = "理想的な状態"
        elif resp_overall > 0.7 and qual_overall < 0.6:
            pattern = "高責任追跡・低品質"
            insight = "プロセスは透明だが説明品質に課題"
        else:
            pattern = "要改善"
            insight = "改善が必要"
        
        correlation_analysis = {
            'correlation_score': correlation_score,
            'pattern': pattern,
            'insight': insight,
            'responsibility_score': resp_overall,
            'quality_score': qual_overall
        }
        
        unified_score = (resp_overall * self.weights['responsibility'] + 
                        qual_overall * self.weights['quality'])
        
        recommendations = []
        if responsibility_result.missing_components:
            recommendations.append(f"責任追跡改善: {', '.join(responsibility_result.missing_components)}")
        if qual_overall < 0.7:
            recommendations.append("品質改善: 説明の詳細化")
        if not recommendations:
            recommendations.append("現状維持")
        
        if unified_score >= 0.9:
            level = "優秀"
        elif unified_score >= 0.75:
            level = "良好"
        else:
            level = "要改善"
        
        overall_assessment = f"統合評価: {level} (スコア: {unified_score:.1%})"
        
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

def main():
    print("統合SRTA評価システム - テスト")
    print("=" * 50)
    
    unified_evaluator = UnifiedSRTAEvaluationLayer()
    
    test_context = {
        'explanation_text': """
This image classification decision was executed based on predefined quality criteria.
Decision Process:
1. Dataset: ImageNet pre-trained model usage
2. Processing: ResNet-50 architecture feature extraction  
3. Criteria: Confidence threshold 87% or higher
For example, triangular ear shapes are characteristic of felines.
Responsible: AI System Administrator (ID: SYS001)
        """.strip(),
        'actor_type': 'hybrid',
        'responsible_entity': 'AI System Administrator'
    }
    
    try:
        result = unified_evaluator.comprehensive_evaluate(test_context)
        
        print(f"\\n統合評価結果:")
        print(f"   統合スコア: {result.unified_score:.1%}")
        print(f"   相関パターン: {result.correlation_analysis['pattern']}")
        print(f"   処理時間: {result.processing_time:.3f}s")
        
        print(f"\\n責任追跡分析:")
        resp = result.responsibility_analysis
        print(f"   レベル: {resp['level']}")
        print(f"   総合スコア: {resp['metrics']['overall']:.1%}")
        
        print(f"\\n品質評価:")
        qual = result.quality_assessment
        print(f"   レベル: {qual['quality_level']}")
        print(f"   総合スコア: {qual['metrics']['overall']:.1%}")
        
        print(f"\\n統合推奨事項:")
        for rec in result.recommendations:
            print(f"   • {rec}")
        
        print(f"\\n総合評価: {result.overall_assessment}")
        print(f"\\n統合システム動作確認完了!")
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
