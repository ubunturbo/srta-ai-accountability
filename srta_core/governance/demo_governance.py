#!/usr/bin/env python3
"""
Governance Core Demo - Shows real-time policy enforcement
Demonstrates how governance differs from logging by modifying system behavior
"""

import sys
import json
from pathlib import Path

# Add the governance module to path
sys.path.insert(0, str(Path(__file__).parent))

from governance_core import GovernanceCore, Policy, Evidence, Action


def create_demo_policies():
    """Create example policies for different domains"""
    return [
        # Safety policies
        Policy(
            id="SAFETY_FACT_MIN",
            owner="Safety",
            signal="fact_score",
            operator=">",
            threshold=0.70,
            severity="review",
            weight=2.0,
            description="Factual accuracy must be above 70% for safety-critical content"
        ),
        
        # Ethics policies
        Policy(
            id="ETHICS_TOX_MAX",
            owner="Ethics",
            signal="toxicity",
            operator="<",
            threshold=0.20,
            severity="block",
            weight=3.0,
            description="Toxicity must be below 20% - blocking threshold"
        ),
        
        # Privacy policies
        Policy(
            id="PRIVACY_PII_MAX",
            owner="Privacy",
            signal="pii_risk",
            operator="<",
            threshold=0.10,
            severity="review",
            weight=1.5,
            description="PII risk must be below 10%"
        ),
        
        # Quality warning
        Policy(
            id="QUALITY_CONF_MIN",
            owner="QualityAssurance",
            signal="confidence",
            operator=">",
            threshold=0.60,
            severity="warn",
            weight=1.0,
            description="Confidence should be above 60% (warning only)"
        )
    ]


def demo_scenario(name: str, signals: dict, expected_action: Action = None):
    """Run a demo scenario and display results"""
    print(f"\n{'='*60}")
    print(f"SCENARIO: {name}")
    print(f"{'='*60}")
    
    # Create governance system
    policies = create_demo_policies()
    actors = ["Safety", "Ethics", "Privacy", "QualityAssurance", "Operations"]
    governance = GovernanceCore(policies=policies, actors=actors)
    
    # Mock content
    prompt = f"Demo query for scenario: {name}"
    output = f"Demo response for scenario: {name}"
    
    # Add mock evidence
    evidences = [
        Evidence(
            kind="retrieval",
            ref="doc:demo_123",
            confidence=0.85,
            metadata={"source": "demo_dataset"}
        )
    ]
    
    print(f"Input signals: {signals}")
    
    # Run governance evaluation
    rtr = governance.evaluate(
        prompt=prompt,
        output=output,
        signals=signals,
        evidences=evidences
    )
    
    # Validate RTR
    is_valid, issues = rtr.validate()
    
    print(f"GOVERNANCE DECISION: {rtr.action.value}")
    print(f"Reason: {rtr.reason}")
    print(f"RTR Valid: {is_valid}")
    if issues:
        print(f"Issues: {issues}")
    
    print(f"\nResponsibility Distribution:")
    for actor, responsibility in sorted(rtr.responsibility.items(), 
                                      key=lambda x: x[1], reverse=True):
        print(f"  {actor}: {responsibility:.2%}")
    
    print(f"\nPolicy Evaluations:")
    for policy_eval in rtr.policies:
        status = "PASS" if policy_eval.passed else "FAIL"
        print(f"  {policy_eval.policy_id}: {status} "
              f"(score: {policy_eval.score}, threshold: {policy_eval.threshold})")
        if policy_eval.reason:
            print(f"    Reason: {policy_eval.reason}")
    
    # Show escalation recommendation
    should_escalate = governance.should_escalate(rtr)
    print(f"\nEscalation Required: {should_escalate}")
    
    if should_escalate:
        responsible_actors = governance.get_responsible_actors(rtr)
        print(f"Responsible Actors (in order): {responsible_actors}")
    
    # Demonstrate behavioral difference from logging
    print(f"\n🔄 BEHAVIORAL IMPACT:")
    if rtr.action == Action.BLOCK:
        print("   ❌ OUTPUT BLOCKED - Would not be shown to user")
        print("   📋 Automatic escalation to responsible teams")
    elif rtr.action == Action.REVIEW:
        print("   ⏸️  OUTPUT HELD FOR REVIEW - Requires approval")
        print("   📋 Assigned to responsible actors for review")
    else:
        print("   ✅ OUTPUT APPROVED - Shown to user immediately")
        if any(p.reason for p in rtr.policies if p.severity == "warn"):
            print("   ⚠️  With warnings logged for improvement")
    
    # Expected vs actual check
    if expected_action and rtr.action != expected_action:
        print(f"\n⚠️  UNEXPECTED RESULT: Expected {expected_action.value}, got {rtr.action.value}")
    
    return rtr


def demo_audit_capabilities(governance: GovernanceCore):
    """Demonstrate audit and reporting capabilities"""
    print(f"\n{'='*60}")
    print("AUDIT CAPABILITIES DEMO")
    print(f"{'='*60}")
    
    # Get audit summary
    summary = governance.get_audit_summary()
    
    print("Governance System Summary:")
    print(f"  Total decisions made: {summary['total_decisions']}")
    print(f"  Policies configured: {summary['policies_evaluated']}")
    
    if summary['action_distribution']:
        print(f"  Action distribution:")
        for action, count in summary['action_distribution'].items():
            print(f"    {action}: {count}")
    
    if summary['responsibility_distribution']:
        print(f"  Responsibility distribution:")
        for actor, total_resp in summary['responsibility_distribution'].items():
            print(f"    {actor}: {total_resp:.2f}")
    
    # Show RTR export capability
    if governance.evaluation_history:
        latest_rtr = governance.evaluation_history[-1]
        print(f"\nSample RTR Export (latest decision):")
        rtr_json = latest_rtr.to_json()
        print(rtr_json[:300] + "..." if len(rtr_json) > 300 else rtr_json)


def main():
    """Run comprehensive governance core demonstration"""
    print("🚀 SRTA Governance Core Demonstration")
    print("Showing real-time policy enforcement vs traditional logging")
    
    # Scenario 1: Clean content - should pass all policies
    demo_scenario(
        "Clean Content",
        {
            "fact_score": 0.85,
            "toxicity": 0.05,
            "pii_risk": 0.02,
            "confidence": 0.90
        },
        expected_action=Action.ALLOW
    )
    
    # Scenario 2: Low factual accuracy - should trigger review
    demo_scenario(
        "Low Factual Accuracy",
        {
            "fact_score": 0.55,  # Below 0.70 threshold
            "toxicity": 0.10,
            "pii_risk": 0.05,
            "confidence": 0.80
        },
        expected_action=Action.REVIEW
    )
    
    # Scenario 3: High toxicity - should block
    demo_scenario(
        "High Toxicity Content",
        {
            "fact_score": 0.90,
            "toxicity": 0.35,  # Above 0.20 threshold
            "pii_risk": 0.08,
            "confidence": 0.75
        },
        expected_action=Action.BLOCK
    )
    
    # Scenario 4: Multiple policy violations
    demo_scenario(
        "Multiple Policy Violations",
        {
            "fact_score": 0.45,  # Below threshold
            "toxicity": 0.25,    # Above threshold  
            "pii_risk": 0.15,    # Above threshold
            "confidence": 0.40   # Below warning threshold
        },
        expected_action=Action.BLOCK  # Block takes precedence
    )
    
    # Scenario 5: Missing signals
    demo_scenario(
        "Missing Signals",
        {
            "confidence": 0.80
            # Missing fact_score, toxicity, pii_risk
        },
        expected_action=Action.BLOCK  # Missing critical signals should block
    )
    
    # Create governance system for audit demo
    policies = create_demo_policies()
    actors = ["Safety", "Ethics", "Privacy", "QualityAssurance", "Operations"]
    governance = GovernanceCore(policies=policies, actors=actors)
    
    # Run audit demo (need to populate some history first)
    governance.evaluate(
        "Audit demo query", 
        "Audit demo output",
        {"fact_score": 0.75, "toxicity": 0.10, "pii_risk": 0.05, "confidence": 0.85}
    )
    
    demo_audit_capabilities(governance)
    
    print(f"\n{'='*60}")
    print("✅ GOVERNANCE CORE DEMONSTRATION COMPLETE")
    print(f"{'='*60}")
    print("Key Differentiators from Traditional Logging:")
    print("1. 🎯 Real-time action determination (ALLOW/REVIEW/BLOCK)")
    print("2. 📊 Quantified responsibility distribution among actors")  
    print("3. 🔄 System behavior modification based on policy evaluation")
    print("4. 📋 Automatic escalation routing to responsible parties")
    print("5. ✅ Complete audit trail with validation")
    
    print("\nNext Steps:")
    print("- Integrate with existing ML pipeline")
    print("- Add approval workflow automation")
    print("- Configure domain-specific policies")
    print("- Set up monitoring and alerting")


if __name__ == "__main__":
    main()
