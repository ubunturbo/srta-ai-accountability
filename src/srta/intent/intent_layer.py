from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


@dataclass
class DesignPrinciple:
    name: str
    stakeholder: str
    weight: float  # 0.0 ~ 1.0
    rationale: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class IntentLayer:
    """
    Minimal spec to satisfy unit tests:
      - principles は {<name>: DesignPrinciple} で保持
      - add_design_principle(name, stakeholder, weight, rationale) -> bool
          * weight が [0.0, 1.0] 以外なら False を返し、登録しない
      - get_applicable_principles(threshold: float = 0.0)
          * weight > threshold の原則を返す（辞書）
      - get_stakeholder_responsibilities(stakeholder)
          * 指定 stakeholder の原則を辞書で返す
      - get_all_principles()
          * 全原則（辞書）を返す（既存互換）
      - validate_principle_consistency()
          * 合計 weight <= 1.0 かを検証し、結果を辞書で返す
    """

    def __init__(self) -> None:
        self.principles: Dict[str, DesignPrinciple] = {}

    # -- CRUD-like operations -------------------------------------------------

    def add_design_principle(
        self,
        name: str,
        stakeholder: str,
        weight: float,
        rationale: str = "",
        overwrite: bool = True,
    ) -> bool:
        """
        Return:
            True  : 追加（または上書き）に成功
            False : weight 不正などで登録しない
        """
        try:
            # 厳密な重み検証（テストが期待）
            if not (0.0 <= float(weight) <= 1.0):
                return False
        except Exception:
            return False

        if (not overwrite) and (name in self.principles):
            return True  # 既存を維持

        self.principles[name] = DesignPrinciple(
            name=name,
            stakeholder=stakeholder,
            weight=float(weight),
            rationale=rationale or "",
        )
        return True

    def remove_design_principle(self, name: str) -> bool:
        if name in self.principles:
            del self.principles[name]
            return True
        return False

    def get_all_principles(self) -> Dict[str, DesignPrinciple]:
        return dict(self.principles)

    # -- Queries used by tests ------------------------------------------------

    def get_applicable_principles(
        self, threshold: float = 0.0
    ) -> Dict[str, DesignPrinciple]:
        """
        threshold より大きい weight の原則を返す。
        """
        try:
            thr = float(threshold)
        except Exception:
            thr = 0.0
        return {k: v for k, v in self.principles.items() if v.weight > thr}

    def get_stakeholder_responsibilities(
        self, stakeholder: str
    ) -> Dict[str, DesignPrinciple]:
        """
        指定 stakeholder に紐づく原則を返す。
        """
        key = (stakeholder or "").strip().lower()
        return {
            name: dp
            for name, dp in self.principles.items()
            if dp.stakeholder.strip().lower() == key
        }

    # -- Validation -----------------------------------------------------------

    def validate_principle_consistency(self) -> Dict[str, float | bool]:
        """
        合計 weight <= 1.0 かを検証。
        戻り値:
          {
            "ok": bool,
            "total_weight": float,
            "excess": float  # 0 以上。超過がなければ 0.0
          }
        """
        total = sum(dp.weight for dp in self.principles.values())
        excess = max(0.0, total - 1.0)
        return {"ok": excess == 0.0, "total_weight": total, "excess": excess}
