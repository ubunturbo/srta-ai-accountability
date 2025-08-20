"""
SRTA Responsibility Tracker Module
責任追跡・透明性評価モジュール
"""

import time
import re
import logging
from typing import Dict, List, Any
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

@dataclass
class ResponsibilityResult:
    metrics: ResponsibilityMetrics
    level: ResponsibilityLevel
    traceable_components: List[str]
    missing_components: List[str]
    assessment_message: str
    processing_time: float
    
    def __getitem__(self, key: str) -> Any:
        """辞書アクセス対応"""
        return getattr(self, key)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式での結果取得"""
        return {
            'metrics': {
                'decision_traceability': self.metrics.decision_traceability,
                'data_lineage': self.metrics.data_lineage,
                'actor_identification': self.metrics.actor_identification,
                'process_transparency': self.metrics.process_transparency,
                'overall': self.metrics.overall
            },
            'level': self.level.value,
            'traceable_components': self.traceable_components,
            'missing_components': self.missing_components,
            'assessment_message': self.assessment_message,
            'processing_time': self.processing_time
        }

class ResponsibilityTracker:
    """責任追跡評価システム"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.responsibility_thresholds = self.config.get('responsibility_thresholds', {
            ResponsibilityLevel.FULLY_TRACEABLE: 0.9,
            ResponsibilityLevel.MOSTLY_TRACEABLE: 0.75,
            ResponsibilityLevel.PARTIALLY_TRACEABLE: 0.6,
            ResponsibilityLevel.NOT_TRACEABLE: 0.4
        })
        logger.info("🔗 SRTA Responsibility Tracker initialized")
    
    def evaluate(self, context: Dict[str, Any]) -> ResponsibilityResult:
        """責任追跡の評価実行"""
        start_time = time.time()
        
        # 責任追跡メトリクスの計算
        decision_trace = self._evaluate_decision_traceability(context)
        data_lineage = self._evaluate_data_lineage(context)
        actor_id = self._evaluate_actor_identification(context)
        process_trans = self._evaluate_process_transparency(context)
        
        overall = (decision_trace + data_lineage + actor_id + process_trans) / 4
        
        metrics = ResponsibilityMetrics(
            decision_traceability=decision_trace,
            data_lineage=data_lineage,
            actor_identification=actor_id,
            process_transparency=process_trans,
            overall=overall
        )
        
        level = self._determine_responsibility_level(overall)
        traceable = self._identify_traceable_components(context, metrics)
        missing = self._identify_missing_components(context, metrics)
        message = self._generate_responsibility_message(level)
        
        return ResponsibilityResult(
            metrics=metrics,
            level=level,
            traceable_components=traceable,
            missing_components=missing,
            assessment_message=message,
            processing_time=time.time() - start_time
        )
    
    def _evaluate_decision_traceability(self, context: Dict[str, Any]) -> float:
        """意思決定の追跡可能性評価"""
        text = context.get('explanation_text', '')
        base_score = 0.5
        
        # 決定プロセスの明示
        if any(word in text.lower() for word in ['decision', 'chose', 'selected', 'determined']):
            base_score += 0.2
        
        # 判断根拠の明示
        if any(word in text.lower() for word in ['based on', 'according to', 'criteria', 'threshold']):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _evaluate_data_lineage(self, context: Dict[str, Any]) -> float:
        """データ系譜の追跡可能性評価"""
        text = context.get('explanation_text', '')
        base_score = 0.4
        
        # データソースの言及
        if any(word in text.lower() for word in ['data', 'dataset', 'source', 'input']):
            base_score += 0.3
        
        # 処理過程の説明
        if any(word in text.lower() for word in ['processed', 'analyzed', 'transformed']):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _evaluate_actor_identification(self, context: Dict[str, Any]) -> float:
        """関与者特定の明確性評価"""
        base_score = 0.6
        
        # システム/人間の明示
        if context.get('actor_type') in ['human', 'system', 'hybrid']:
            base_score += 0.2
        
        # 責任者の明示
        if context.get('responsible_entity'):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _evaluate_process_transparency(self, context: Dict[str, Any]) -> float:
        """プロセス透明性の評価"""
        text = context.get('explanation_text', '')
        base_score = 0.5
        
        # プロセス説明の存在
        if any(word in text.lower() for word in ['process', 'method', 'algorithm']):
            base_score += 0.2
        
        # ステップの明示
        if re.search(r'\d+\.|step|phase|stage', text.lower()):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _determine_responsibility_level(self, score: float) -> ResponsibilityLevel:
        """責任追跡レベルの決定"""
        for level in [ResponsibilityLevel.FULLY_TRACEABLE, ResponsibilityLevel.MOSTLY_TRACEABLE, 
                      ResponsibilityLevel.PARTIALLY_TRACEABLE]:
            if score >= self.responsibility_thresholds[level]:
                return level
        return ResponsibilityLevel.NOT_TRACEABLE
    
    def _identify_traceable_components(self, context: Dict[str, Any], metrics: ResponsibilityMetrics) -> List[str]:
        """追跡可能なコンポーネントの特定"""
        traceable = []
        if metrics.decision_traceability > 0.7:
            traceable.append("意思決定プロセス")
        if metrics.data_lineage > 0.7:
            traceable.append("データ系譜")
        if metrics.actor_identification > 0.7:
            traceable.append("関与者特定")
        if metrics.process_transparency > 0.7:
            traceable.append("プロセス透明性")
        return traceable
    
    def _identify_missing_components(self, context: Dict[str, Any], metrics: ResponsibilityMetrics) -> List[str]:
        """不足コンポーネントの特定"""
        missing = []
        if metrics.decision_traceability <= 0.7:
            missing.append("意思決定根拠の明示")
        if metrics.data_lineage <= 0.7:
            missing.append("データソース情報")
        if metrics.actor_identification <= 0.7:
            missing.append("責任者情報")
        if metrics.process_transparency <= 0.7:
            missing.append("処理プロセス詳細")
        return missing
    
    def _generate_responsibility_message(self, level: ResponsibilityLevel) -> str:
        """責任追跡メッセージ生成"""
        messages = {
            ResponsibilityLevel.FULLY_TRACEABLE: "完全な責任追跡が可能で、監査要件を満たしています。",
            ResponsibilityLevel.MOSTLY_TRACEABLE: "概ね責任追跡が可能ですが、一部改善の余地があります。",
            ResponsibilityLevel.PARTIALLY_TRACEABLE: "部分的な責任追跡のみ可能で、重要な情報が不足しています。",
            ResponsibilityLevel.NOT_TRACEABLE: "責任追跡が困難で、透明性の大幅な改善が必要です。"
        }
        return messages[level]

def main():
    """責任追跡モジュールのテスト"""
    print("🔗 SRTA Responsibility Tracker Module Test")
    tracker = ResponsibilityTracker()
    
    test_context = {
        'explanation_text': """
Decision: Image classified as 'cat' based on CNN analysis.
Data source: ImageNet training dataset, processed through ResNet-50.
Decision criteria: Confidence threshold set at 87%.
Responsible system: AI Classification Module v2.1
        """.strip(),
        'actor_type': 'system',
        'responsible_entity': 'AI Classification Module'
    }
    
    result = tracker.evaluate(test_context)
    
    print(f"\n📊 Responsibility Analysis:")
    print(f"   Decision Traceability: {result.metrics.decision_traceability:.1%}")
    print(f"   Data Lineage: {result.metrics.data_lineage:.1%}")
    print(f"   Actor Identification: {result.metrics.actor_identification:.1%}")
    print(f"   Process Transparency: {result.metrics.process_transparency:.1%}")
    print(f"   Overall: {result.metrics.overall:.1%}")
    print(f"🏆 Responsibility Level: {result.level.value}")
    print(f"✅ Traceable: {', '.join(result.traceable_components)}")
    print(f"❌ Missing: {', '.join(result.missing_components)}")
    print(f"📝 Assessment: {result.assessment_message}")
    print("\nResponsibility Tracker working! ✅")

if __name__ == "__main__":
    main()
