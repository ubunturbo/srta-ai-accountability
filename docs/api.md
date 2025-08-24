# SRTA API リファレンス

## EvaluationLayer

### クラス: EvaluationLayer()

AI生成説明の品質を評価するメインクラス

#### メソッド

##### evaluate_explanation(data: dict) -> EvaluationResult

説明文の品質を評価します。

**パラメータ:**
- `data` (dict): 評価対象データ
  - `explanation_text` (str): 評価する説明文

**戻り値:**
- `EvaluationResult`: 評価結果オブジェクト
  - `metrics.overall` (float): 総合品質スコア (0.0-1.0)
  - `quality_level.value` (str): 品質レベル ("Poor", "Fair", "Good", "Excellent")
  - `improvement_suggestions` (list): 改善提案

**使用例:**
```python
from src.srta.evaluation.evaluation_layer import EvaluationLayer

evaluator = EvaluationLayer()
result = evaluator.evaluate_explanation({
    'explanation_text': 'この画像は猫と判定されました。'
})
print(f"スコア: {result.metrics.overall:.1%}")
