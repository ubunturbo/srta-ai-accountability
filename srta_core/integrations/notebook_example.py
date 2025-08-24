"""Jupyter Notebook Integration for SRTA Governance"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir / "governance"))

from governance_core import GovernanceCore, Policy, Evidence, Action

class NotebookGovernanceWrapper:
    def __init__(self, policies: List[Policy] = None, actors: List[str] = None):
        if policies is None:
            policies = [
                Policy(id="NOTEBOOK_QUALITY", owner="DataScience", signal="confidence", 
                      operator=">", threshold=0.5, severity="warn", weight=1.0),
                Policy(id="NOTEBOOK_SAFETY", owner="Safety", signal="toxicity", 
                      operator="<", threshold=0.4, severity="block", weight=2.0)
            ]
        
        if actors is None:
            actors = ["DataScience", "Safety", "Operations"]
        
        self.governance = GovernanceCore(policies=policies, actors=actors)
        self.results_log = []
    
    def evaluate_output(self, prompt: str, output: str, signals: Dict[str, float] = None) -> Dict[str, Any]:
        if signals is None:
            signals = {}
        
        # Auto-compute missing signals
        if "confidence" not in signals:
            signals["confidence"] = 0.8 if len(output) > 10 else 0.4
        if "toxicity" not in signals:
            toxic_words = ['hate', 'kill', 'violence']
            signals["toxicity"] = sum(1 for word in toxic_words if word in output.lower()) / 10.0
        
        rtr = self.governance.evaluate(prompt=prompt, output=output, signals=signals)
        
        result = {
            "prompt": prompt,
            "output": output,
            "signals": signals,
            "action": rtr.action.value,
            "reason": rtr.reason,
            "responsibility": rtr.responsibility,
            "audit_id": rtr.decision_id
        }
        
        self.results_log.append(result)
        return result

def quick_governance_check(output: str, prompt: str = "") -> str:
    wrapper = NotebookGovernanceWrapper()
    result = wrapper.evaluate_output(prompt, output)
    return result['action']

def example_usage():
    print("=== Notebook Integration Demo ===")
    wrapper = NotebookGovernanceWrapper()
    
    test_cases = [
        ("What's AI?", "AI is machine learning technology."),
        ("Tell me about people", "I hate everyone and want violence."),
        ("Hi", "Hello!")
    ]
    
    for prompt, output in test_cases:
        result = wrapper.evaluate_output(prompt, output)
        print(f"Input: {output}")
        print(f"Decision: {result['action']}")
        print(f"Reason: {result['reason']}")
        print("---")

if __name__ == "__main__":
    example_usage()
