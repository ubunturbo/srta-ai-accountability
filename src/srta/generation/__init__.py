"""
SRTA Generation Layer Package
AI決定の説明文を生成するパッケージ
"""

from .generation_layer import (
    GenerationLayer,
    GenerationContext,
    ExplanationStyle,
    GeneratedExplanation
)

__version__ = "0.1.0"
__author__ = "SRTA Project"

# パッケージレベルでエクスポートするクラス・関数
__all__ = [
    "GenerationLayer",
    "GenerationContext", 
    "ExplanationStyle",
    "GeneratedExplanation"
]
