# SRTA: Structured Reasoning and Transparency Architecture

AI生成説明の品質を評価するためのPythonフレームワーク

## 機能
- 説明文の明確性、完全性、理解しやすさを数値評価
- 改善提案の自動生成
- 高速処理（1ms未満）
- モジュラー設計で拡張可能

## 使用例
```python
from src.srta.evaluation.evaluation_layer import EvaluationLayer

evaluator = EvaluationLayer()
result = evaluator.evaluate_explanation({
    'explanation_text': 'この画像は猫と判定されました。形状と質感の特徴により87%の信頼度です。'
})

print(f"品質スコア: {result.metrics.overall:.1%}")
print(f"品質レベル: {result.quality_level.value}")
git clone https://github.com/ubunturbo/srta-ai-accountability.git
cd srta-ai-accountability
python benchmarks/quick_check.py
