# SRTA チュートリアル

## インストール

```bash
git clone https://github.com/ubunturbo/srta-ai-accountability.git
cd srta-ai-accountability
from src.srta.evaluation.evaluation_layer import EvaluationLayer

# 評価器を作成
evaluator = EvaluationLayer()

# 説明文を評価
result = evaluator.evaluate_explanation({
    'explanation_text': 'この画像は猫と判定されました。'
})

# 結果を表示
print(f"品質スコア: {result.metrics.overall:.1%}")
print(f"レベル: {result.quality_level.value}")
