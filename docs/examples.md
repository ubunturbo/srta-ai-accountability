# SRTA 使用例集

## 基本的な使用例

### 1. 簡単な説明文の評価

```python
from src.srta.evaluation.evaluation_layer import EvaluationLayer

evaluator = EvaluationLayer()

# 基本的な評価
result = evaluator.evaluate_explanation({
    'explanation_text': 'この画像は猫と判定されました。形状と質感の特徴により87%の信頼度です。'
})

print(f"品質スコア: {result.metrics.overall:.1%}")
print(f"品質レベル: {result.quality_level.value}")
print("改善提案:", result.improvement_suggestions)
