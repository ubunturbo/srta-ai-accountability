from typing import Dict, Any, List
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class EvaluationResult:
    score: float
    criteria_scores: Dict[str, float]
    explanations: List[str]
    recommendations: List[str]

class ResponsibilityEvaluator:
    def __init__(self, criteria_weights: Dict[str, float] = None):
        self.criteria_weights = criteria_weights or {
            'traceability': 0.3,
            'accountability': 0.3,
            'transparency': 0.2,
            'fairness': 0.2
        }
    
    def evaluate(self, explanation: str, context: Dict[str, Any]) -> EvaluationResult:
        try:
            criteria_scores = self._evaluate_criteria(explanation, context)
            overall_score = sum(
                score * self.criteria_weights.get(criterion, 0)
                for criterion, score in criteria_scores.items()
            )
            
            explanations = self._generate_explanations(criteria_scores)
            recommendations = self._generate_recommendations(criteria_scores)
            
            return EvaluationResult(
                score=overall_score,
                criteria_scores=criteria_scores,
                explanations=explanations,
                recommendations=recommendations
            )
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            raise ValueError(f"Cannot evaluate explanation: {e}")
    
    def _evaluate_criteria(self, explanation: str, context: Dict[str, Any]) -> Dict[str, float]:
        scores = {}
        
        # Traceability: presence of decision steps
        has_steps = any(indicator in explanation.lower() for indicator in ['step', 'first', 'then', 'because'])
        scores['traceability'] = 0.8 if has_steps else 0.3
        
        # Accountability: actor identification
        has_actor = context.get('actor_id') is not None
        scores['accountability'] = 0.9 if has_actor else 0.2
        
        # Transparency: explanation length and detail
        word_count = len(explanation.split())
        scores['transparency'] = min(1.0, word_count / 50.0)
        
        # Fairness: bias indicators
        bias_terms = ['always', 'never', 'all', 'none']
        has_bias = any(term in explanation.lower() for term in bias_terms)
        scores['fairness'] = 0.4 if has_bias else 0.8
        
        return scores
    
    def _generate_explanations(self, criteria_scores: Dict[str, float]) -> List[str]:
        explanations = []
        for criterion, score in criteria_scores.items():
            if score < 0.5:
                explanations.append(f"Low {criterion} score ({score:.2f}) indicates improvement needed")
        return explanations
    
    def _generate_recommendations(self, criteria_scores: Dict[str, float]) -> List[str]:
        recommendations = []
        if criteria_scores.get('traceability', 0) < 0.5:
            recommendations.append("Add step-by-step reasoning to improve traceability")
        if criteria_scores.get('transparency', 0) < 0.5:
            recommendations.append("Provide more detailed explanations")
        return recommendations
