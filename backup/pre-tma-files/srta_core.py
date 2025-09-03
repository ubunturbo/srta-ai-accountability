"""
SRTA-Core: Responsibility Tracing Implementation
Core schema and attribution logic for deployable responsibility tracking
"""

import json
import re
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime

@dataclass
class Attribution:
    """Links output chunks to supporting evidence with weights"""
    output: str
    evidence: List[str]
    weights: List[float]
    confidence: float = 0.0

@dataclass
class Metrics:
    """Quality metrics for the generation process"""
    evidence_coverage: float
    evidence_precision: float
    hallucination_rate: float
    attribution_confidence: float = 0.0

@dataclass
class PolicyDecision:
    """Policy decision for content delivery"""
    delivery: str  # "pass", "needs_review", "reject"
    reasons: List[str]
    actions: Optional[List[str]] = None

def tokenize_simple(text: str) -> List[str]:
    """Simple tokenization for coverage calculation"""
    return re.findall(r'\b\w+\b', text.lower())

def fuzzy_ngram_match(text1: str, text2: str, n: int = 3) -> float:
    """Calculate fuzzy n-gram overlap between two texts"""
    tokens1 = tokenize_simple(text1)
    tokens2 = tokenize_simple(text2)
    
    if not tokens1 or not tokens2:
        return 0.0
    
    ngrams1 = set(' '.join(tokens1[i:i+n]) for i in range(len(tokens1) - n + 1))
    ngrams2 = set(' '.join(tokens2[i:i+n]) for i in range(len(tokens2) - n + 1))
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    return intersection / union if union > 0 else 0.0

def calculate_attribution(output_text: str, evidence_texts: List[str]) -> Attribution:
    """Calculate attribution weights for output text given evidence"""
    if not evidence_texts:
        return Attribution(output="", evidence=[], weights=[], confidence=0.0)
    
    scores = []
    for evidence in evidence_texts:
        score = fuzzy_ngram_match(output_text, evidence)
        scores.append(max(0.0, score))
    
    total_score = sum(scores)
    if total_score > 0:
        weights = [s / total_score for s in scores]
    else:
        weights = [1.0 / len(evidence_texts)] * len(evidence_texts)
    
    confidence = max(scores) if scores else 0.0
    
    return Attribution(
        output=output_text,
        evidence=evidence_texts,
        weights=weights,
        confidence=confidence
    )

def calculate_metrics(output_text: str, attributions: List[Attribution]) -> Metrics:
    """Calculate evidence coverage and precision metrics"""
    if not output_text or not attributions:
        return Metrics(
            evidence_coverage=0.0,
            evidence_precision=0.0,
            hallucination_rate=1.0
        )
    
    tokens = tokenize_simple(output_text)
    total_tokens = len(tokens)
    
    # Simple coverage: high confidence attributions cover the text
    covered_tokens = 0
    for attr in attributions:
        if attr.confidence > 0.7:
            attr_tokens = tokenize_simple(attr.output)
            covered_tokens += len(attr_tokens)
    
    coverage = min(1.0, covered_tokens / total_tokens) if total_tokens > 0 else 0.0
    
    # Precision: proportion of high-confidence attributions
    high_conf_attrs = sum(1 for attr in attributions if attr.confidence > 0.7)
    precision = high_conf_attrs / len(attributions) if attributions else 0.0
    
    hallucination_rate = 1.0 - coverage
    avg_confidence = sum(attr.confidence for attr in attributions) / len(attributions) if attributions else 0.0
    
    return Metrics(
        evidence_coverage=coverage,
        evidence_precision=precision,
        hallucination_rate=hallucination_rate,
        attribution_confidence=avg_confidence
    )

def make_policy_decision(metrics: Metrics) -> PolicyDecision:
    """Make policy decision based on metrics"""
    reasons = []
    delivery = "pass"
    actions = []
    
    if metrics.evidence_coverage < 0.6:
        reasons.append("coverage_below_threshold")
        delivery = "needs_review"
        actions.append("request_more_evidence")
    
    if metrics.evidence_precision < 0.7:
        reasons.append("precision_below_threshold")
        if delivery != "reject":
            delivery = "needs_review"
        actions.append("verify_evidence_quality")
    
    if metrics.hallucination_rate > 0.3:
        reasons.append("high_hallucination_rate")
        delivery = "reject"
        actions.append("regenerate_with_constraints")
    
    if not reasons:
        reasons.append("all_thresholds_met")
    
    return PolicyDecision(
        delivery=delivery,
        reasons=reasons,
        actions=actions if actions else None
    )

def create_responsibility_manifest(output_text: str, evidence_texts: List[str]) -> Dict[str, Any]:
    """Create complete responsibility manifest for given output and evidence"""
    
    # Calculate attribution
    attribution = calculate_attribution(output_text, evidence_texts)
    
    # Calculate metrics
    metrics = calculate_metrics(output_text, [attribution])
    
    # Make policy decision
    policy = make_policy_decision(metrics)
    
    # Create manifest
    manifest = {
        "version": "1.0",
        "task_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "attribution": asdict(attribution),
        "metrics": asdict(metrics),
        "policy": asdict(policy)
    }
    
    return manifest

if __name__ == "__main__":
    print("SRTA-Core Responsibility Tracing Test")
    print("=" * 40)
    
    # Test case 1: High-quality attribution
    output1 = "The capital of France is Paris."
    evidence1 = ["Paris is the capital and most populous city of France."]
    
    print("\nTest 1: High-quality evidence")
    manifest1 = create_responsibility_manifest(output1, evidence1)
    
    print(f"Output: {output1}")
    print(f"Evidence: {evidence1[0]}")
    print(f"Attribution confidence: {manifest1['attribution']['confidence']:.3f}")
    print(f"Evidence coverage: {manifest1['metrics']['evidence_coverage']:.3f}")
    print(f"Policy decision: {manifest1['policy']['delivery']}")
    print(f"Reasons: {manifest1['policy']['reasons']}")
    
    # Test case 2: Low-quality attribution
    output2 = "The weather will be sunny tomorrow with temperatures reaching 25°C."
    evidence2 = ["Paris is the capital and most populous city of France."]
    
    print("\nTest 2: Poor evidence match")
    manifest2 = create_responsibility_manifest(output2, evidence2)
    
    print(f"Output: {output2}")
    print(f"Evidence: {evidence2[0]}")
    print(f"Attribution confidence: {manifest2['attribution']['confidence']:.3f}")
    print(f"Evidence coverage: {manifest2['metrics']['evidence_coverage']:.3f}")
    print(f"Policy decision: {manifest2['policy']['delivery']}")
    print(f"Reasons: {manifest2['policy']['reasons']}")
    
    # Test case 3: Multiple evidence sources
    output3 = "Paris is the capital of France and has a population of over 2 million people."
    evidence3 = [
        "Paris is the capital and most populous city of France.",
        "The city proper has a population of 2,161,000 residents."
    ]
    
    print("\nTest 3: Multiple evidence sources")
    manifest3 = create_responsibility_manifest(output3, evidence3)
    
    print(f"Output: {output3}")
    print(f"Evidence sources: {len(evidence3)}")
    print(f"Attribution weights: {[f'{w:.3f}' for w in manifest3['attribution']['weights']]}")
    print(f"Attribution confidence: {manifest3['attribution']['confidence']:.3f}")
    print(f"Evidence coverage: {manifest3['metrics']['evidence_coverage']:.3f}")
    print(f"Policy decision: {manifest3['policy']['delivery']}")
    
    print(f"\nManifest JSON (first 200 chars):")
    json_output = json.dumps(manifest3, indent=2)
    print(json_output[:200] + "...")
