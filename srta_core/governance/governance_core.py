"""
SRTA Governance Core - Real-time Policy Enforcement and Responsibility Distribution
The key differentiator: Runtime behavior modification, not just logging
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime, timezone
import hashlib
import json


class Action(str, Enum):
    """Governance actions that modify system behavior"""
    ALLOW = "ALLOW"
    REVIEW = "REVIEW" 
    BLOCK = "BLOCK"


@dataclass
class Policy:
    """Policy definition with ownership and enforcement rules"""
    id: str
    owner: str                  # Responsible party: "Safety", "Ethics", "Privacy"
    signal: str                 # Signal to evaluate: "toxicity", "fact_score", etc.
    operator: str               # Comparison operator: "<", ">", "=="
    threshold: float            # Threshold value
    severity: str               # Action level: "warn", "review", "block"
    weight: float = 1.0         # Weight for responsibility distribution
    description: str = ""       # Human-readable policy description


@dataclass 
class Evidence:
    """Evidence supporting a decision"""
    kind: str                   # Type: "retrieval", "tool_output", "human_input"
    ref: str                    # Reference: ID, URL, path
    confidence: float = 1.0     # Confidence in this evidence
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyEval:
    """Result of evaluating a single policy"""
    policy_id: str
    owner: str
    passed: bool
    score: Optional[float]
    operator: str
    threshold: float
    severity: str
    reason: str
    weight: float = 1.0


@dataclass
class RTR:
    """Responsibility Trace Record - Complete audit trail for one decision"""
    decision_id: str
    timestamp: str
    request_hash: str
    output_hash: str
    signals: Dict[str, float]
    policies: List[PolicyEval]
    responsibility: Dict[str, float]  # owner -> responsibility_weight
    action: Action
    reason: str
    evidences: List[Evidence] = field(default_factory=list)
    audit: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate RTR completeness and consistency"""
        issues = []
        
        # Required fields check
        required_fields = [
            "decision_id", "timestamp", "request_hash", "output_hash",
            "signals", "policies", "responsibility", "action"
        ]
        for field_name in required_fields:
            value = getattr(self, field_name, None)
            if value in (None, "", {}, []):
                issues.append(f"missing_required_field:{field_name}")
        
        # Responsibility distribution validation
        if self.responsibility:
            total = sum(self.responsibility.values())
            if not (0.99 <= total <= 1.01):
                issues.append(f"responsibility_sum_invalid:{total:.3f}")
            
            # Check for negative responsibilities
            negative_resp = [k for k, v in self.responsibility.items() if v < 0]
            if negative_resp:
                issues.append(f"negative_responsibility:{negative_resp}")
        
        # Hash format validation (basic check)
        for hash_field in [self.request_hash, self.output_hash]:
            if not isinstance(hash_field, str) or len(hash_field) < 16:
                issues.append("invalid_hash_format")
                break
        
        # Policy consistency check
        if self.policies:
            policy_owners = {p.owner for p in self.policies}
            resp_owners = set(self.responsibility.keys()) if self.responsibility else set()
            
            # All policy owners should have some responsibility assignment
            missing_owners = policy_owners - resp_owners
            if missing_owners and len(self.policies) > 0:
                issues.append(f"missing_responsibility_for_owners:{list(missing_owners)}")
        
        return (len(issues) == 0, issues)

    def to_json(self, indent: int = 2) -> str:
        """Export RTR as JSON string"""
        data = asdict(self)
        return json.dumps(data, ensure_ascii=False, indent=indent)


class GovernanceCore:
    """
    Core governance engine that enforces policies in real-time
    
    Key difference from logging: This system modifies behavior based on policy evaluation,
    rather than just recording events after they happen.
    """
    
    def __init__(self, policies: List[Policy], actors: List[str]):
        self.policies = {p.id: p for p in policies}  # Index by ID for faster lookup
        self.actors = set(actors)
        self.evaluation_history: List[RTR] = []
        
        # Validate policy configuration
        self._validate_policies()
    
    def _validate_policies(self) -> None:
        """Validate policy configuration at initialization"""
        policy_owners = {p.owner for p in self.policies.values()}
        unknown_owners = policy_owners - self.actors
        if unknown_owners:
            raise ValueError(f"Unknown policy owners: {unknown_owners}. "
                           f"Must be in actors list: {self.actors}")
    
    @staticmethod
    def _hash_content(content: Any) -> str:
        """Generate deterministic hash for content"""
        if isinstance(content, str):
            data = content
        else:
            data = json.dumps(content, sort_keys=True, ensure_ascii=False)
        
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
    
    def _evaluate_policy(self, policy: Policy, signals: Dict[str, float]) -> PolicyEval:
        """Evaluate a single policy against provided signals"""
        signal_value = signals.get(policy.signal)
        passed = True
        reason = ""
        
        if signal_value is None:
            passed = False
            reason = f"signal_missing:{policy.signal}"
        else:
            # Evaluate based on operator
            if policy.operator == "<":
                condition_met = signal_value < policy.threshold
            elif policy.operator == ">":
                condition_met = signal_value > policy.threshold
            elif policy.operator == "==":
                condition_met = abs(signal_value - policy.threshold) < 0.001
            elif policy.operator == "<=":
                condition_met = signal_value <= policy.threshold
            elif policy.operator == ">=":
                condition_met = signal_value >= policy.threshold
            else:
                passed = False
                reason = f"unsupported_operator:{policy.operator}"
                condition_met = False
            
            # Determine pass/fail based on severity and condition
            if policy.severity == "warn":
                # Warnings always "pass" but generate reasons
                passed = True
                if not condition_met:
                    reason = f"warning_condition_not_met:{signal_value}_{policy.operator}_{policy.threshold}"
            else:
                # Review and block policies must meet conditions to pass
                passed = condition_met
                if not passed:
                    reason = f"condition_failed:{signal_value}_{policy.operator}_{policy.threshold}"
        
        return PolicyEval(
            policy_id=policy.id,
            owner=policy.owner,
            passed=passed,
            score=signal_value,
            operator=policy.operator,
            threshold=policy.threshold,
            severity=policy.severity,
            reason=reason,
            weight=policy.weight
        )
    
    def _determine_action(self, evaluations: List[PolicyEval]) -> Tuple[Action, str]:
        """Determine final action based on policy evaluations"""
        
        # Separate by severity
        blocking_failures = [e for e in evaluations if not e.passed and e.severity == "block"]
        review_failures = [e for e in evaluations if not e.passed and e.severity == "review"]
        warnings = [e for e in evaluations if e.severity == "warn" and e.reason]
        
        # Decision logic: block > review > warn > allow
        if blocking_failures:
            failed_policies = [e.policy_id for e in blocking_failures]
            responsible_owners = sorted(set(e.owner for e in blocking_failures))
            return (
                Action.BLOCK,
                f"blocked_by_policies:{failed_policies}_owners:{responsible_owners}"
            )
        
        if review_failures:
            failed_policies = [e.policy_id for e in review_failures]
            responsible_owners = sorted(set(e.owner for e in review_failures))
            return (
                Action.REVIEW,
                f"review_required_policies:{failed_policies}_owners:{responsible_owners}"
            )
        
        if warnings:
            warning_policies = [e.policy_id for e in warnings]
            return (
                Action.ALLOW,
                f"allowed_with_warnings:{warning_policies}"
            )
        
        return (Action.ALLOW, "all_policies_passed")
    
    def _distribute_responsibility(self, evaluations: List[PolicyEval]) -> Dict[str, float]:
        """
        Distribute responsibility among actors based on policy failures and warnings
        
        Logic: Actors responsible for failed/warning policies get weighted responsibility
        If no issues, responsibility defaults to "Operations"
        """
        responsibility_scores: Dict[str, float] = {}
        
        # Collect weighted scores for actors with policy issues
        for evaluation in evaluations:
            if evaluation.reason:  # Has failure or warning
                current_score = responsibility_scores.get(evaluation.owner, 0.0)
                
                # Weight responsibility by policy weight and severity
                severity_multiplier = {
                    "block": 3.0,
                    "review": 2.0, 
                    "warn": 1.0
                }.get(evaluation.severity, 1.0)
                
                responsibility_scores[evaluation.owner] = (
                    current_score + evaluation.weight * severity_multiplier
                )
        
        # If no issues found, assign to default operations
        if not responsibility_scores:
            return {"Operations": 1.0}
        
        # Normalize to sum to 1.0
        total_score = sum(responsibility_scores.values())
        return {
            owner: score / total_score 
            for owner, score in responsibility_scores.items()
        }
    
    def evaluate(
        self,
        prompt: str,
        output: str,
        signals: Dict[str, float],
        evidences: Optional[List[Evidence]] = None,
        decision_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RTR:
        """
        Main evaluation method - determines action and responsibility distribution
        
        This is where governance differs from logging: the returned action should
        be used to modify system behavior (allow/review/block the output)
        """
        
        # Generate metadata
        timestamp = datetime.now(timezone.utc).isoformat()
        request_hash = self._hash_content({"prompt": prompt})
        output_hash = self._hash_content({"output": output})
        decision_id = decision_id or output_hash[:16]
        
        # Evaluate all policies
        evaluations = [
            self._evaluate_policy(policy, signals) 
            for policy in self.policies.values()
        ]
        
        # Determine action and responsibility
        action, reason = self._determine_action(evaluations)
        responsibility = self._distribute_responsibility(evaluations)
        
        # Create audit trail
        audit_info = {
            "evaluation_count": len(evaluations),
            "failed_policies": len([e for e in evaluations if not e.passed]),
            "chain_hash": self._hash_content({
                "request": request_hash,
                "output": output_hash,
                "timestamp": timestamp
            })
        }
        
        # Create RTR
        rtr = RTR(
            decision_id=decision_id,
            timestamp=timestamp,
            request_hash=request_hash,
            output_hash=output_hash,
            signals=signals,
            policies=evaluations,
            responsibility=responsibility,
            action=action,
            reason=reason,
            evidences=evidences or [],
            audit=audit_info,
            metadata=metadata or {}
        )
        
        # Store in history
        self.evaluation_history.append(rtr)
        
        return rtr
    
    def get_responsible_actors(self, rtr: RTR) -> List[str]:
        """Get list of actors responsible for this decision, sorted by responsibility"""
        return sorted(
            rtr.responsibility.keys(),
            key=lambda actor: rtr.responsibility[actor],
            reverse=True
        )
    
    def should_escalate(self, rtr: RTR, escalation_threshold: float = 0.5) -> bool:
        """Determine if this decision should be escalated to human review"""
        return (
            rtr.action in [Action.REVIEW, Action.BLOCK] or
            max(rtr.responsibility.values()) > escalation_threshold
        )
    
    def get_audit_summary(self, limit: int = 10) -> Dict[str, Any]:
        """Get summary of recent governance decisions"""
        recent_rtrs = self.evaluation_history[-limit:] if self.evaluation_history else []
        
        action_counts = {}
        responsibility_totals = {}
        
        for rtr in recent_rtrs:
            # Count actions
            action_counts[rtr.action.value] = action_counts.get(rtr.action.value, 0) + 1
            
            # Sum responsibility by actor
            for actor, resp in rtr.responsibility.items():
                responsibility_totals[actor] = responsibility_totals.get(actor, 0.0) + resp
        
        return {
            "total_decisions": len(recent_rtrs),
            "action_distribution": action_counts,
            "responsibility_distribution": responsibility_totals,
            "policies_evaluated": len(self.policies)
        }
