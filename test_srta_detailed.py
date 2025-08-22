from srta import SRTASystem

def test_detailed():
    system = SRTASystem()
    
    # Test case 1: Good explanation
    result1 = system.evaluate_explanation(
        explanation="The model classified this as a cat because it detected triangular ears and whiskers through CNN analysis.",
        context={'actor_id': 'model_v1.0', 'confidence': 0.95}
    )
    
    print("=== Test 1: Good Explanation ===")
    eval_result = result1['evaluation']
    print(f"Overall score: {eval_result.score:.2f}")
    print("Criteria scores:")
    for criterion, score in eval_result.criteria_scores.items():
        print(f"  {criterion}: {score:.2f}")
    print(f"Recommendations: {eval_result.recommendations}")
    print(f"Audit hash: {result1['audit_hash'][:8]}...")
    print()
    
    # Test case 2: Poor explanation
    result2 = system.evaluate_explanation(
        explanation="It's a cat.",
        context={'confidence': 0.60}
    )
    
    print("=== Test 2: Poor Explanation ===")
    eval_result2 = result2['evaluation']
    print(f"Overall score: {eval_result2.score:.2f}")
    print("Criteria scores:")
    for criterion, score in eval_result2.criteria_scores.items():
        print(f"  {criterion}: {score:.2f}")
    print(f"Recommendations: {eval_result2.recommendations}")
    print()
    
    print(f"Audit trail integrity: {system.audit_trail.verify_integrity()}")
    print(f"Total audit entries: {len(system.audit_trail.entries)}")

if __name__ == "__main__":
    test_detailed()
