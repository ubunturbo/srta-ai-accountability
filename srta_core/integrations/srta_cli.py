#!/usr/bin/env python3
"""SRTA Governance CLI Tool"""

import argparse
import json
import sys
from pathlib import Path

# Fix import path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir / "governance"))

from governance_core import GovernanceCore, Policy, Evidence, Action

class GovernanceCLI:
    def __init__(self):
        self.governance = None
    
    def create_default_config(self, output_file: str):
        """Create a default configuration file"""
        config = {
            "actors": ["Safety", "Quality", "Operations"],
            "policies": [
                {
                    "id": "SAFETY_TEST", "owner": "Safety", "signal": "toxicity",
                    "operator": "<", "threshold": 0.3, "severity": "block", "weight": 2.0
                },
                {
                    "id": "QUALITY_TEST", "owner": "Quality", "signal": "confidence",
                    "operator": ">", "threshold": 0.6, "severity": "warn", "weight": 1.0
                }
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created config: {output_file}")
    
    def load_config(self, config_file: str):
        """Load governance configuration"""
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        policies = []
        for p in config.get('policies', []):
            policies.append(Policy(
                id=p['id'], owner=p['owner'], signal=p['signal'],
                operator=p['operator'], threshold=p['threshold'],
                severity=p['severity'], weight=p.get('weight', 1.0)
            ))
        
        actors = config.get('actors', [])
        self.governance = GovernanceCore(policies=policies, actors=actors)
        print(f"Loaded {len(policies)} policies")
    
    def evaluate_single(self, prompt: str, output: str, signals: dict):
        """Evaluate single prompt/output"""
        if not self.governance:
            print("No config loaded")
            return
        
        rtr = self.governance.evaluate(prompt=prompt, output=output, signals=signals)
        
        print(f"Decision: {rtr.action.value}")
        print(f"Reason: {rtr.reason}")
        print("Responsibility:", rtr.responsibility)
    
    def test_policies(self):
        """Test governance policies"""
        test_cases = [
            ("Hello", "Hi there!", {"confidence": 0.8, "toxicity": 0.1}),
            ("Bad words", "I hate everything!", {"confidence": 0.7, "toxicity": 0.8}),
            ("Unsure", "Maybe?", {"confidence": 0.3, "toxicity": 0.0})
        ]
        
        for prompt, output, signals in test_cases:
            print(f"\nTesting: {output}")
            self.evaluate_single(prompt, output, signals)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help="Config file")
    parser.add_argument('--create-config', help="Create default config")
    
    subparsers = parser.add_subparsers(dest='command')
    
    eval_parser = subparsers.add_parser('eval')
    eval_parser.add_argument('--prompt', '-p', required=True)
    eval_parser.add_argument('--output', '-o', required=True)
    eval_parser.add_argument('--signals', '-s', help="JSON signals")
    
    test_parser = subparsers.add_parser('test')
    
    args = parser.parse_args()
    cli = GovernanceCLI()
    
    if args.create_config:
        cli.create_default_config(args.create_config)
        return
    
    if args.config:
        cli.load_config(args.config)
    
    if args.command == 'eval':
        signals = json.loads(args.signals) if args.signals else {}
        cli.evaluate_single(args.prompt, args.output, signals)
    elif args.command == 'test':
        cli.test_policies()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
