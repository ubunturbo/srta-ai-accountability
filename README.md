# SRTA: AI Explanation Evaluation Framework

⚠️ **Proof-of-Concept Architecture** - A research framework for systematic evaluation of AI explanations, combining quality assessment with responsibility tracking.

## Contribution Type

This repository presents a novel architectural approach to AI explanation accountability, demonstrating how responsibility tracking can be integrated with quality assessment. The implementation serves as a proof-of-concept for the theoretical framework rather than a validated production system.

## Architectural Innovation

- Integration of stakeholder attribution with explanation evaluation
- Multi-layer principle tracking (Authority, Interface, Integration modules)  
- Structured accountability assessment alongside traditional quality metrics
- Proof-of-concept implementation demonstrating architectural feasibility

## Research Positioning

This work contributes to the theoretical understanding of responsibility-aware AI systems rather than claiming empirical validation. The focus is on architectural patterns and implementation feasibility, providing a foundation for future validation studies by researchers with appropriate resources.


## What SRTA Does

SRTA evaluates existing AI explanations by measuring both their quality and the level of responsibility information they contain. The system provides statistical analysis of how these two aspects correlate and offers recommendations for improvement.

**Core functionality:**
- Quality assessment: Measures clarity, completeness, and understandability of explanations
- Responsibility tracking: Evaluates presence of actor identification, decision traceability, and process transparency
- Correlation analysis: Analyzes statistical relationships between quality and responsibility metrics
- Pattern classification: Categorizes evaluation results into improvement patterns

## What SRTA Does Not Do

- Does not generate explanations (evaluates existing ones only)
- Does not provide legal compliance verification
- Does not include cryptographic audit trails or blockchain features
- Does not implement natural language processing or semantic analysis

## Usage Example

```python
from src.srta.evaluation.evaluation_layer import EvaluationLayer

# Initialize evaluator
config = {'weights': {'responsibility': 0.6, 'quality': 0.4}}
evaluator = EnhancedUnifiedSRTAEvaluationLayer(config)

# Evaluate an explanation
context = {
    'explanation_text': 'The model classified this as a cat based on detected features...',
    'actor_id': 'classification_model_v1',
    'responsible_entity': 'ML Team'
}

result = evaluator.comprehensive_evaluate(context)
print(f"Quality score: {result.quality_assessment['overall']:.1%}")
print(f"Responsibility score: {result.responsibility_analysis['overall']:.1%}")


Installation and Testing
bashgit clone https://github.com/ubunturbo/srta-ai-accountability.git
cd srta-ai-accountability

# Test the system
python src/srta/evaluation/unified_evaluation_final.py
Limitations
- **Platform**: Windows compatibility may vary (tested primarily on Linux/macOS)

- **Scope**: Evaluation tool only, not a complete XAI solution
- **Scale**: Tested on limited scenarios, not validated on large datasets
- **Analysis**: Statistical correlation, not causal inference
- **Integration**: Standalone tool, requires manual integration with existing systems
- **Validation**: Research implementation, not production-ready software

Project Status
Research implementation - functional but not production-ready
Last Updated: August 2025

## Public API Contract
The file `docs/contracts/public_api_contract.yaml` describes the expected public API.
It is **not an executable test**, but serves as a contract specification for integration testing or schema validation.
