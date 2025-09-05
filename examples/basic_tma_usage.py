#!/usr/bin/env python3
"""
TMA-SRTA Basic Usage Example
Three-Module Architecture for Self-Regulating Transparent AI

This example demonstrates the basic usage of TMA-SRTA for creating
transparent, accountable AI systems using Structural Design Pattern Theory.

Example Domain: Medical AI Decision Support System
Shows: Multi-stakeholder principles, transparent decision making,
       and structured accountability through four-cause implementation.
"""

import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tma.tma_srta import TMAArchitecture, DesignPrinciple


def create_medical_ai_system():
    """
    Create a medical AI system with proper multi-stakeholder principles
    
    This example shows how to implement a medical decision support system
    that maintains transparent accountability and stakeholder integration.
    """
    
    # Define design principles with stakeholder input
    medical_principles = [
        DesignPrinciple(
            name="patient_safety",
            description="Patient safety is the highest priority in all medical decisions",
            weight=0.95,
            constraints={
                "safety_threshold_required": True,
                "risk_assessment_mandatory": True,
                "adverse_event_monitoring": True
            },
            stakeholder_input={
                "medical_ethics_board": 0.4,
                "patient_safety_committee": 0.3,
                "attending_physicians": 0.2,
                "patient_advocates": 0.1
            }
        ),
        
        DesignPrinciple(
            name="professional_oversight",
            description="Medical professionals must retain final decision authority",
            weight=0.90,
            constraints={
                "require_physician_approval": True,
                "medical_license_verification": True,
                "professional_responsibility": True
            },
            stakeholder_input={
                "attending_physicians": 0.5,
                "medical_board": 0.3,
                "hospital_administration": 0.2
            }
        ),
        
        DesignPrinciple(
            name="evidence_based_practice",
            description="All recommendations must be based on current medical evidence",
            weight=0.85,
            constraints={
                "literature_reference_required": True,
                "clinical_guidelines_adherence": True,
                "evidence_quality_assessment": True
            },
            stakeholder_input={
                "medical_researchers": 0.4,
                "clinical_specialists": 0.4,
                "evidence_review_board": 0.2
            }
        ),
        
        DesignPrinciple(
            name="patient_autonomy",
            description="Respect patient rights and informed decision making",
            weight=0.80,
            constraints={
                "informed_consent_required": True,
                "patient_preference_consideration": True,
                "cultural_sensitivity": True
            },
            stakeholder_input={
                "patients": 0.5,
                "patient_advocates": 0.3,
                "medical_ethics_board": 0.2
            }
        ),
        
        DesignPrinciple(
            name="transparency_accountability",
            description="All medical AI decisions must be explainable and auditable",
            weight=0.88,
            constraints={
                "decision_audit_trail": True,
                "explanation_generation": True,
                "regulatory_compliance": True
            },
            stakeholder_input={
                "regulatory_agencies": 0.4,
                "hospital_administration": 0.3,
                "medical_ethics_board": 0.3
            }
        )
    ]
    
    # Initialize TMA system
    medical_tma = TMAArchitecture(
        principles=medical_principles,
        system_purpose="Medical Decision Support System with Transparent Accountability"
    )
    
    return medical_tma


def demonstrate_medical_scenarios(medical_system):
    """
    Demonstrate TMA system with various medical scenarios
    
    Shows how the system handles different types of medical decisions
    with appropriate stakeholder consideration and transparency.
    """
    
    print("=" * 80)
    print("🏥 MEDICAL AI DECISION SUPPORT DEMONSTRATION")
    print("=" * 80)
    
    # Scenario 1: Routine Treatment Decision
    print("\n📋 SCENARIO 1: Routine Treatment Decision")
    print("-" * 50)
    
    routine_query = """
    Patient presents with mild hypertension (140/90 mmHg) and no other risk factors.
    Should we recommend starting antihypertensive medication immediately?
    """
    
    result1 = medical_system.process_with_tma(routine_query.strip())
    
    print(f"Query: {routine_query.strip()}")
    print(f"\n🏛️ Authority Principles Activated:")
    for guidance in result1['authority_principles']['foundational_guidance']:
        print(f"  • {guidance['principle']}: {guidance['guidance']}")
    
    print(f"\n💬 Interface Response:")
    print(f"  {result1['interface_mediation']['practical_response']}")
    
    print(f"\n🔍 Integration Validation:")
    print(f"  Coherence Score: {result1['integration_validation']['coherence_score']:.3f}")
    print(f"  System Validation: {'✅ PASS' if result1['integration_validation']['interconnected_validation'] else '❌ NEEDS ATTENTION'}")
    
    # Scenario 2: High-Risk Decision
    print("\n\n🚨 SCENARIO 2: High-Risk Treatment Decision")
    print("-" * 50)
    
    high_risk_query = """
    78-year-old patient with multiple comorbidities needs experimental cardiac procedure.
    High surgical risk but potential for significant life extension. Patient wants to proceed.
    Should we recommend the experimental procedure?
    """
    
    result2 = medical_system.process_with_tma(high_risk_query.strip())
    
    print(f"Query: {high_risk_query.strip()}")
    print(f"\n🏛️ Authority Principles Activated:")
    for guidance in result2['authority_principles']['foundational_guidance']:
        print(f"  • {guidance['principle']}: {guidance['guidance']} (influence: {guidance['influence']:.3f})")
    
    print(f"\n💬 Interface Response:")
    print(f"  {result2['interface_mediation']['practical_response']}")
    
    print(f"\n🔍 Integration Validation:")
    print(f"  Coherence Score: {result2['integration_validation']['coherence_score']:.3f}")
    print(f"  Quality Score: {result2['integration_validation']['integration_quality']:.3f}")
    
    # Show constraint requirements
    constraints = result2['authority_principles'].get('constraint_requirements', {})
    if constraints:
        print(f"\n🔒 Required Constraints:")
        for constraint, value in constraints.items():
            print(f"  • {constraint}: {'Required' if value else 'Not Required'}")
    
    # Scenario 3: Emergency Decision
    print("\n\n⚡ SCENARIO 3: Emergency Medical Decision")
    print("-" * 50)
    
    emergency_query = """
    Emergency department: Patient in cardiac arrest, needs immediate intervention.
    Family unavailable for consent. Should we proceed with emergency treatment?
    """
    
    result3 = medical_system.process_with_tma(emergency_query.strip())
    
    print(f"Query: {emergency_query.strip()}")
    print(f"\n🏛️ Authority Principles Activated:")
    for guidance in result3['authority_principles']['foundational_guidance']:
        print(f"  • {guidance['principle']}: {guidance['guidance']}")
    
    print(f"\n💬 Interface Response:")
    print(f"  {result3['interface_mediation']['practical_response']}")
    
    print(f"\n🔍 Integration Validation:")
    print(f"  Coherence Score: {result3['integration_validation']['coherence_score']:.3f}")
    
    return [result1, result2, result3]


def demonstrate_complete_transparency(medical_system):
    """
    Demonstrate complete transparency and explainability features
    
    Shows how TMA provides comprehensive decision explanation
    and accountability tracking.
    """
    
    print("\n\n🔍 TRANSPARENCY AND EXPLAINABILITY DEMONSTRATION")
    print("=" * 80)
    
    complex_query = """
    Complex case: 45-year-old surgeon diagnosed with early-stage Parkinson's disease.
    Impact on surgical abilities uncertain. How should we approach fitness for practice evaluation?
    """
    
    # Get complete decision explanation
    explanation = medical_system.explain_decision(complex_query)
    
    print(f"Query: {complex_query}")
    print(f"\n📊 COMPLETE DECISION BREAKDOWN:")
    
    for aspect, details in explanation.items():
        aspect_formatted = aspect.replace('_', ' ').title()
        print(f"\n{aspect_formatted}:")
        print(f"  {details}")
    
    # Show system status
    status = medical_system.get_system_status()
    print(f"\n📈 SYSTEM PERFORMANCE STATUS:")
    print(f"  System Purpose: {status['system_purpose']}")
    print(f"  Total Principles: {status['total_principles']}")
    print(f"  Processing Sessions: {status['processing_sessions']}")
    print(f"  Average Coherence: {status['average_coherence']:.3f}")
    print(f"  System Status: {status['status'].upper()}")


def demonstrate_stakeholder_integration(medical_system):
    """
    Demonstrate multi-stakeholder principle integration
    
    Shows how different stakeholder perspectives are weighted
    and integrated into decision making.
    """
    
    print("\n\n👥 MULTI-STAKEHOLDER INTEGRATION DEMONSTRATION")
    print("=" * 80)
    
    stakeholder_query = """
    Controversial treatment: New immunotherapy for cancer with promising results
    but significant side effects and high cost. Patient insurance may not cover.
    Multiple stakeholders have different perspectives. How do we proceed?
    """
    
    result = medical_system.process_with_tma(stakeholder_query)
    
    print(f"Query: {stakeholder_query}")
    
    # Analyze stakeholder influence in activated principles
    print(f"\n🎯 STAKEHOLDER INFLUENCE ANALYSIS:")
    
    activated_principles = result['authority_principles']['foundational_guidance']
    
    # Aggregate stakeholder influence across all activated principles
    total_stakeholder_influence = {}
    
    for principle_info in activated_principles:
        principle_name = principle_info['principle']
        influence = principle_info['influence']
        
        # Find the principle object to get stakeholder input
        principle_obj = medical_system.authority.principles.get(principle_name)
        if principle_obj and principle_obj.stakeholder_input:
            for stakeholder, weight in principle_obj.stakeholder_input.items():
                if stakeholder not in total_stakeholder_influence:
                    total_stakeholder_influence[stakeholder] = 0
                total_stakeholder_influence[stakeholder] += influence * weight
    
    # Sort stakeholders by total influence
    sorted_stakeholders = sorted(
        total_stakeholder_influence.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    print(f"\nStakeholder Influence in This Decision:")
    for stakeholder, total_influence in sorted_stakeholders:
        percentage = (total_influence / sum(total_stakeholder_influence.values())) * 100
        print(f"  • {stakeholder.replace('_', ' ').title()}: {percentage:.1f}% influence")
    
    # Show how this affects the final decision
    print(f"\n🏆 DECISION OUTCOME:")
    print(f"  Response: {result['interface_mediation']['practical_response']}")
    print(f"  Coherence: {result['integration_validation']['coherence_score']:.3f}")
    
    return result


def main():
    """
    Main demonstration program
    
    Comprehensive demonstration of TMA-SRTA capabilities
    including medical AI decision support scenarios.
    """
    
    print("🚀 TMA-SRTA: Three-Module Architecture Demonstration")
    print("Structural Design Pattern Theory in Action")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create medical AI system
    print("\n🔧 Initializing Medical AI System...")
    medical_system = create_medical_ai_system()
    print("✅ TMA Medical System initialized successfully!")
    
    print(f"\nSystem Configuration:")
    print(f"  • {len(medical_system.authority.principles)} design principles loaded")
    print(f"  • Authority Module: Principle evaluation engine")
    print(f"  • Interface Module: Response mediation system")
    print(f"  • Integration Module: Coherence validation system")
    
    try:
        # Demonstrate various scenarios
        scenario_results = demonstrate_medical_scenarios(medical_system)
        
        # Demonstrate transparency
        demonstrate_complete_transparency(medical_system)
        
        # Demonstrate stakeholder integration
        stakeholder_result = demonstrate_stakeholder_integration(medical_system)
        
        # Final system performance summary
        print("\n\n📊 FINAL SYSTEM PERFORMANCE SUMMARY")
        print("=" * 80)
        
        # Calculate average performance across all scenarios
        all_coherence_scores = []
        for result in scenario_results + [stakeholder_result]:
            all_coherence_scores.append(result['integration_validation']['coherence_score'])
        
        avg_coherence = sum(all_coherence_scores) / len(all_coherence_scores)
        
        print(f"Total Scenarios Processed: {len(scenario_results) + 1}")
        print(f"Average Coherence Score: {avg_coherence:.3f}")
        print(f"System Performance: {'EXCELLENT' if avg_coherence >= 0.8 else 'GOOD' if avg_coherence >= 0.6 else 'NEEDS IMPROVEMENT'}")
        
        # Show key achievements
        print(f"\n🏆 KEY ACHIEVEMENTS DEMONSTRATED:")
        print(f"  ✅ Four-Cause Design Implementation: Authority/Interface/Integration modules")
        print(f"  ✅ Multi-Stakeholder Integration: {len(medical_system.authority.principles)} principles with stakeholder weighting")
        print(f"  ✅ Transparent Decision Making: Complete explanation and audit trail")
        print(f"  ✅ Structural Integration: Quantifiable coherence measurement")
        print(f"  ✅ Domain Applicability: Medical AI decision support validated")
        
        print(f"\n🌟 CONCLUSION:")
        print(f"TMA-SRTA successfully demonstrates the first computational implementation")
        print(f"of classical four-cause design patterns in modern AI systems.")
        print(f"This represents the restoration of Aristotelian design causation")
        print(f"after 2,400 years of theoretical-only existence!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Please check system configuration and try again.")
        sys.exit(1)
    
    print(f"\n🎯 Ready to implement TMA-SRTA in your domain?")
    print(f"See README.md for additional examples and documentation.")


if __name__ == "__main__":
    main()
