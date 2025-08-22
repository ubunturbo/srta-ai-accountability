from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class DesignPrinciple:
    name: str
    stakeholder: str
    weight: float  # 0.0 ~ 1.0
    justification: str = ""  # tests expect this field name

    # 互換性: もし外部から rationale を参照したい場合に備えた別名
    @property
    def rationale(self) -> str:
        return self.justification

    def to_dict(self) -> Dict:
        return asdict(self)


class IntentLayer:
    """
    Unit tests expectation:
      - principles: {<name>: DesignPrinciple}
      - stakeholder_map: {<stakeholder>: [<principle_name>, ...]}
      - add_design_principle(name, stakeholder, weight, justification) -> bool
          * weight ∈ [0.0, 1.0] 以外は False で登録しない
      - get_applicable_principles(threshold=0.0) -> dict[name, DesignPrinciple]
      - get_stakeholder_responsibilities(stakeholder) -> dict[name, DesignPrinciple]
      - get_all_principles() -> dict[name, DesignPrinciple]
      - validate_principle_consistency() -> {"is_consistent": bool, "total_weight": float, "excess": float}
    """

    def __init__(self) -> None:
        self.principles: Dict[str, DesignPrinciple] = {}
        self.stakeholder_map: Dict[str, List[str]] = {}

    # -- CRUD-like operations -------------------------------------------------

    def add_design_principle(
        self,
        name: str,
        stakeholder: str,
        weight: float,
        justification: str = "",
        overwrite: bool = True,
    ) -> bool:
        try:
            w = float(weight)
        except Exception:
            return False
        if not (0.0 <= w <= 1.0):
            return False

        if (not overwrite) and (name in self.principles):
            return True  # keep existing

        # 既存の stakeholder 紐付けを掃除（名前で上書きする場合を考慮）
        if name in self.principles:
            old = self.principles[name]
            if old.stakeholder in self.stakeholder_map:
                self.stakeholder_map[old.stakeholder] = [
                    n for n in self.stakeholder_map[old.stakeholder] if n != name
                ]
                if not self.stakeholder_map[old.stakeholder]:
                    del self.stakeholder_map[old.stakeholder]

        self.principles[name] = DesignPrinciple(
            name=name,
            stakeholder=stakeholder,
            weight=w,
            justification=justification or "",
        )

        # stakeholder_map を更新
        key = stakeholder.strip()
        self.stakeholder_map.setdefault(key, [])
        if name not in self.stakeholder_map[key]:
            self.stakeholder_map[key].append(name)

        return True

    def remove_design_principle(self, name: str) -> bool:
        if name in self.principles:
            dp = self.principles[name]
            del self.principles[name]
            if dp.stakeholder in self.stakeholder_map:
                self.stakeholder_map[dp.stakeholder] = [
                    n for n in self.stakeholder_map[dp.stakeholder] if n != name
                ]
                if not self.stakeholder_map[dp.stakeholder]:
                    del self.stakeholder_map[dp.stakeholder]
            return True
        return False

    def get_all_principles(self) -> Dict[str, DesignPrinciple]:
        return dict(self.principles)

    # -- Queries used by tests ------------------------------------------------

    def get_applicable_principles(self, threshold: float = 0.0) -> Dict[str, DesignPrinciple]:
        try:
            thr = float(threshold)
        except Exception:
            thr = 0.0
        return {k: v for k, v in self.principles.items() if v.weight > thr}

    def get_stakeholder_responsibilities(self, stakeholder: str) -> Dict[str, DesignPrinciple]:
        key = (stakeholder or "").strip().lower()
        return {
            name: dp
            for name, dp in self.principles.items()
            if dp.stakeholder.strip().lower() == key
        }

    # -- Validation -----------------------------------------------------------

    def validate_principle_consistency(self) -> Dict[str, float | bool]:
        total = sum(dp.weight for dp in self.principles.values())
        excess = max(0.0, total - 1.0)
        # tests expect 'is_consistent'; 互換のため 'ok' も返す
        return {
            "is_consistent": excess == 0.0,
            "ok": excess == 0.0,
            "total_weight": total,
            "excess": excess,
        }
