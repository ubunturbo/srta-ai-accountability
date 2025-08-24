# SRTA Governance Core

A Python implementation for AI system governance with policy-based decision control.

## What This Is

A governance layer that evaluates actions against policies and tracks responsibility. Currently a prototype.

## Files

- `srta_core/governance/governance_core.py` - Main engine
- `srta_core/governance/demo_governance.py` - Demo script
- `srta_core/integrations/` - Integration examples

## Usage

```python
from srta_core.governance.governance_core import SRTAGovernanceCore

core = SRTAGovernanceCore()
result = core.evaluate(
    action="process_payment",
    context={"amount": 1000}
)
print(result['decision'])  # ALLOW, REVIEW, or BLOCK
