from srta.intent.intent_layer import IntentLayer

def main():
    intent = IntentLayer()
    print("[INIT] created_at:", intent.created_at.isoformat())

    # 原則を2つ登録
    ok1 = intent.add_design_principle(
        name="fairness",
        stakeholder="AI Ethics Team",
        weight=0.6,
        justification="EU AI Act compliance"
    )
    ok2 = intent.add_design_principle(
        name="safety",
        stakeholder="Safety Board",
        weight=0.5,  # 合計>1.0にして consistency=NG を体験
        justification="Incident prevention"
    )
    print(f"[ADD] fairness={ok1}, safety={ok2}")

    # 適用可能原則の一覧（しきい値 0.0）
    applicable = intent.get_applicable_principles()
    print("[APPLICABLE]", list(applicable.keys()))

    # ステークホルダー単位の責務
    team_a = intent.get_stakeholder_responsibilities("AI Ethics Team")
    print("[RESPONSIBILITIES][AI Ethics Team]", list(team_a.keys()))

    # 一貫性チェック（合計が1.0を超えているのでNG想定）
    validation = intent.validate_principle_consistency()
    print("[VALIDATION]", validation)

if __name__ == "__main__":
    main()
