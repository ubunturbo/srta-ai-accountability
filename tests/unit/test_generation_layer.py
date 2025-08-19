"""
Generation Layer ユニットテスト (pytest不要版)
"""

import sys
import os
from datetime import datetime

# パスを追加してモジュールをインポート
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from srta.generation.generation_layer import (
    GenerationLayer,
    GenerationContext,
    ExplanationStyle,
    GeneratedExplanation
)


def test_generation_context():
    """GenerationContext のテスト"""
    print("🧪 GenerationContext テスト")
    
    # デフォルトコンテキストの確認
    context = GenerationContext()
    assert context.user_background == "general"
    assert context.explanation_style == ExplanationStyle.SIMPLE
    assert context.max_length == 200
    assert context.include_confidence is True
    assert context.language == "ja"
    print("  ✅ デフォルトコンテキスト OK")
    
    # カスタムコンテキストの確認
    context = GenerationContext(
        user_background="expert",
        explanation_style=ExplanationStyle.TECHNICAL,
        max_length=500,
        include_confidence=False
    )
    assert context.user_background == "expert"
    assert context.explanation_style == ExplanationStyle.TECHNICAL
    assert context.max_length == 500
    assert context.include_confidence is False
    print("  ✅ カスタムコンテキスト OK")


def test_generation_layer_basic():
    """GenerationLayer の基本テスト"""
    print("\n🧪 GenerationLayer 基本テスト")
    
    # 初期化テスト
    layer = GenerationLayer()
    assert layer.context is not None
    assert isinstance(layer.template_library, dict)
    print("  ✅ 初期化 OK")
    
    # テンプレート読み込みテスト
    templates = layer.template_library
    required_templates = [
        "decision_template",
        "confidence_template", 
        "reasoning_template",
        "uncertainty_template"
    ]
    
    for template_name in required_templates:
        assert template_name in templates
        assert isinstance(templates[template_name], str)
        assert len(templates[template_name]) > 0
    print("  ✅ テンプレート読み込み OK")


def test_explanation_generation():
    """説明生成のテスト"""
    print("\n🧪 説明生成テスト")
    
    layer = GenerationLayer()
    
    # サンプルデータ
    sample_intent_analysis = {
        "primary_intent": "テキスト分類: ポジティブ",
        "confidence_score": 0.89,
        "key_factors": ["感情語", "構文パターン", "文脈"],
        "data_quality": 0.95,
        "pattern_confidence": 0.82,
        "uncertainty_sources": ["語彙の曖昧性"]
    }
    
    # 説明生成
    explanation = layer.generate_explanation(sample_intent_analysis)
    
    # 結果確認
    assert isinstance(explanation, GeneratedExplanation)
    assert explanation.main_explanation is not None
    assert len(explanation.main_explanation) > 0
    assert isinstance(explanation.confidence_score, float)
    assert isinstance(explanation.reasoning_steps, list)
    assert isinstance(explanation.metadata, dict)
    assert explanation.generation_timestamp is not None
    
    print(f"  ✅ 説明生成 OK: {explanation.main_explanation[:50]}...")
    print(f"  ✅ 信頼度: {explanation.confidence_score}")
    print(f"  ✅ 推論ステップ数: {len(explanation.reasoning_steps)}")


def test_context_customization():
    """コンテキストカスタマイズテスト"""
    print("\n🧪 コンテキストカスタマイズテスト")
    
    layer = GenerationLayer()
    
    # 初期値確認
    assert layer.context.max_length == 200
    assert layer.context.explanation_style == ExplanationStyle.SIMPLE
    
    # カスタマイズ実行
    layer.customize_context(
        max_length=250,
        explanation_style=ExplanationStyle.DETAILED
    )
    
    # 更新確認
    assert layer.context.max_length == 250
    assert layer.context.explanation_style == ExplanationStyle.DETAILED
    
    print("  ✅ コンテキストカスタマイズ OK")


def run_all_tests():
    """全テストを実行"""
    print("=== Generation Layer Unit Tests ===")
    
    try:
        test_generation_context()
        test_generation_layer_basic()
        test_explanation_generation()
        test_context_customization()
        
        print("\n🎉 全テスト PASSED! ✅")
        return True
        
    except Exception as e:
        print(f"\n❌ テスト失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # 手動テスト実行
    success = run_all_tests()
    
    if success:
        print("\n=== 追加テスト例 ===")
        
        # 基本機能テスト
        layer = GenerationLayer()
        
        sample_data = {
            "primary_intent": "感情分析: 喜び",
            "confidence_score": 0.91,
            "key_factors": ["感情語", "絵文字", "文体"],
            "data_quality": 0.88,
            "pattern_confidence": 0.93
        }
        
        explanation = layer.generate_explanation(sample_data)
        
        print(f"✅ 基本生成テスト: {explanation.main_explanation}")
        print(f"✅ 信頼度テスト: {explanation.confidence_score}")
        print(f"✅ 推論ステップ数: {len(explanation.reasoning_steps)}")
        print(f"✅ メタデータ確認: {len(explanation.metadata)} keys")
        print(f"✅ タイムスタンプ: {explanation.generation_timestamp}")
        
        print("\nAll manual tests passed! ✅")
