"""
SRTA Generation Layer
AI決定の説明文を生成する基本クラス
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ExplanationStyle(Enum):
    """説明スタイルの種類"""
    SIMPLE = "simple"      # シンプルな説明
    DETAILED = "detailed"  # 詳細な説明
    TECHNICAL = "technical" # 技術的な説明


@dataclass
class GenerationContext:
    """説明生成のコンテキスト情報"""
    user_background: str = "general"  # ユーザーの背景知識レベル
    explanation_style: ExplanationStyle = ExplanationStyle.SIMPLE
    max_length: int = 200  # 最大文字数
    include_confidence: bool = True  # 信頼度を含めるか
    language: str = "ja"  # 言語設定


@dataclass
class GeneratedExplanation:
    """生成された説明の結果"""
    main_explanation: str
    confidence_score: float
    reasoning_steps: List[str]
    metadata: Dict[str, Any]
    generation_timestamp: str


class GenerationLayer:
    """
    AI決定の説明文を生成するメインクラス
    Intent Layer からの分析結果を受け取り、
    人間が理解しやすい説明文に変換する
    """
    
    def __init__(self, context: Optional[GenerationContext] = None):
        """
        Generation Layer を初期化
        
        Args:
            context: 説明生成のコンテキスト設定
        """
        self.context = context or GenerationContext()
        self.template_library = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """説明文のテンプレートを読み込み"""
        return {
            "decision_template": "AIは{factors}を考慮して、{decision}という判断をしました。",
            "confidence_template": "この判断の信頼度は{confidence:.1%}です。",
            "reasoning_template": "主な理由: {reasoning}",
            "uncertainty_template": "不確実性: {uncertainty_factors}"
        }
        
    def generate_explanation(
        self, 
        intent_analysis: Dict[str, Any]
    ) -> GeneratedExplanation:
        """
        Intent分析結果から説明文を生成
        
        Args:
            intent_analysis: Intent Layer からの分析結果
            
        Returns:
            GeneratedExplanation: 生成された説明
        """
        # 基本情報を抽出
        decision = intent_analysis.get("primary_intent", "Unknown")
        confidence = intent_analysis.get("confidence_score", 0.0)
        factors = intent_analysis.get("key_factors", [])
        
        # メイン説明文を生成
        main_explanation = self._generate_main_explanation(
            decision, factors, confidence
        )
        
        # 推論ステップを生成
        reasoning_steps = self._generate_reasoning_steps(intent_analysis)
        
        # メタデータを構築
        metadata = {
            "style": self.context.explanation_style.value,
            "user_background": self.context.user_background,
            "source_analysis": intent_analysis
        }
        
        from datetime import datetime
        
        return GeneratedExplanation(
            main_explanation=main_explanation,
            confidence_score=confidence,
            reasoning_steps=reasoning_steps,
            metadata=metadata,
            generation_timestamp=datetime.now().isoformat()
        )
        
    def _generate_main_explanation(
        self, 
        decision: str, 
        factors: List[str], 
        confidence: float
    ) -> str:
        """メインの説明文を生成"""
        
        # 要因をテキストに変換
        if factors:
            factors_text = "、".join(factors[:3])  # 最初の3つまで
        else:
            factors_text = "複数の要因"
            
        # 基本説明を生成
        base_explanation = self.template_library["decision_template"].format(
            factors=factors_text,
            decision=decision
        )
        
        # 信頼度情報を追加
        if self.context.include_confidence:
            confidence_text = self.template_library["confidence_template"].format(
                confidence=confidence
            )
            explanation = f"{base_explanation} {confidence_text}"
        else:
            explanation = base_explanation
            
        # 長さ制限を適用
        if len(explanation) > self.context.max_length:
            explanation = explanation[:self.context.max_length-3] + "..."
            
        return explanation
        
    def _generate_reasoning_steps(
        self, 
        intent_analysis: Dict[str, Any]
    ) -> List[str]:
        """推論ステップを生成"""
        
        steps = []
        
        # データ分析ステップ
        if "data_quality" in intent_analysis:
            quality = intent_analysis["data_quality"]
            steps.append(f"入力データの品質を評価: {quality:.1%}")
            
        # パターン認識ステップ
        if "pattern_confidence" in intent_analysis:
            pattern_conf = intent_analysis["pattern_confidence"]
            steps.append(f"パターンを識別: 信頼度{pattern_conf:.1%}")
            
        # 意思決定ステップ
        primary_intent = intent_analysis.get("primary_intent", "Unknown")
        steps.append(f"最終判断: {primary_intent}")
        
        return steps
        
    def customize_context(self, **kwargs) -> None:
        """コンテキストを動的に更新"""
        for key, value in kwargs.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)
                
    def get_context_info(self) -> Dict[str, Any]:
        """現在のコンテキスト情報を取得"""
        return asdict(self.context)


# デモ用の実行例
def demo_generation_layer():
    """Generation Layer のデモンストレーション"""
    print("=== SRTA Generation Layer Demo ===")
    
    # サンプルの Intent 分析結果
    sample_intent_analysis = {
        "primary_intent": "画像分類: 猫",
        "confidence_score": 0.87,
        "key_factors": ["形状パターン", "色彩情報", "エッジ検出"],
        "data_quality": 0.92,
        "pattern_confidence": 0.85,
        "uncertainty_sources": ["照明条件", "画像解像度"]
    }
    
    # Generation Layer を初期化
    context = GenerationContext(
        explanation_style=ExplanationStyle.SIMPLE,
        max_length=150,
        include_confidence=True
    )
    
    generator = GenerationLayer(context)
    
    # 説明を生成
    explanation = generator.generate_explanation(sample_intent_analysis)
    
    # 結果を表示
    print(f"メイン説明: {explanation.main_explanation}")
    print(f"信頼度: {explanation.confidence_score:.1%}")
    print("推論ステップ:")
    for i, step in enumerate(explanation.reasoning_steps, 1):
        print(f"  {i}. {step}")
    print(f"生成時刻: {explanation.generation_timestamp}")
    
    print("\n=== スタイル変更デモ ===")
    
    # 詳細スタイルに変更
    generator.customize_context(
        explanation_style=ExplanationStyle.DETAILED,
        max_length=300
    )
    
    detailed_explanation = generator.generate_explanation(sample_intent_analysis)
    print(f"詳細説明: {detailed_explanation.main_explanation}")
    
    print("\nGeneration Layer MVP working! ✅")


if __name__ == "__main__":
    demo_generation_layer()
