# SRTA 統合評価システム - 統合ガイド

## 📋 統合概要

既存の SRTA プロジェクトに責任追跡 + 品質評価の統合システムを追加しました。

## 🔧 追加されたファイル

1. **evaluation_layer_enhanced.py** - 既存evaluation_layer.pyの改良版
   - EvaluationResult subscriptable エラー修正
   - 型安全性・例外処理強化
   - 既存API完全互換

2. **responsibility_tracker.py** - 責任追跡モジュール
   - 意思決定追跡可能性評価
   - データ系譜追跡
   - 関与者特定
   - プロセス透明性評価

3. **unified_evaluation_layer.py** - 統合評価システム
   - 責任追跡 + 品質評価の統合
   - 相関分析機能
   - 統合スコア計算
   - 包括的推奨事項生成

## 🚀 使用方法

### 1. 既存システムの改良版使用
```python
from src.srta.evaluation.evaluation_layer_enhanced import EvaluationLayer

evaluator = EvaluationLayer()
result = evaluator.evaluate_explanation(context)
# subscriptable エラー解決済み
print(result['quality_level'])
```

### 2. 統合システム使用
```python
from src.srta.evaluation.unified_evaluation_layer import UnifiedSRTAEvaluationLayer

unified_evaluator = UnifiedSRTAEvaluationLayer()
result = unified_evaluator.comprehensive_evaluate(context)
print(f"統合スコア: {result.unified_score:.1%}")
```

### 3. 既存APIとの互換性
```python
# 既存コードはそのまま動作
result = unified_evaluator.evaluate_explanation(context)  # 互換性維持
```

## 📊 評価結果の構造

### 統合評価結果
- quality_assessment: 品質評価結果
- responsibility_analysis: 責任追跡結果  
- correlation_analysis: 相関分析
- unified_score: 統合スコア
- recommendations: 統合推奨事項
- overall_assessment: 総合評価

## 🔄 段階的導入

1. **Phase 1**: evaluation_layer_enhanced.py でエラー修正
2. **Phase 2**: responsibility_tracker.py で責任追跡機能追加
3. **Phase 3**: unified_evaluation_layer.py で完全統合
4. **Phase 4**: 既存システムの置き換え（オプション）

## ⚙️ 設定オプション

```python
config = {
    'weights': {'responsibility': 0.6, 'quality': 0.4},
    'quality_thresholds': {...},
    'responsibility_thresholds': {...}
}
```

## 🧪 テスト実行

```bash
# 個別モジュールテスト
python ./src/srta/evaluation/evaluation_layer_enhanced.py
python ./src/srta/evaluation/responsibility_tracker.py
python ./src/srta/evaluation/unified_evaluation_layer.py
```
