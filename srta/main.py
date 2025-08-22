import logging
from typing import Dict, Any
from .core.audit_trail import AuditTrail
from .evaluation.evaluator import ResponsibilityEvaluator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SRTASystem:
    def __init__(self):
        self.audit_trail = AuditTrail()
        self.evaluator = ResponsibilityEvaluator()
    
    def evaluate_explanation(self, explanation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = self.evaluator.evaluate(explanation, context)
            
            audit_hash = self.audit_trail.add_entry(
                actor_id=context.get('actor_id', 'unknown'),
                action='explanation_evaluation',
                input_data={'explanation': explanation, 'context': context},
                output_data=result,
                metadata={'system_version': '1.0'}
            )
            
            return {
                'evaluation': result,
                'audit_hash': audit_hash,
                'integrity_verified': self.audit_trail.verify_integrity()
            }
        
        except Exception as e:
            logger.error(f"System evaluation failed: {e}")
            return {'error': str(e)}

def main():
    system = SRTASystem()
    
    result = system.evaluate_explanation(
        explanation="The model classified this as a cat because it detected triangular ears and whiskers.",
        context={'actor_id': 'model_v1.0', 'confidence': 0.95}
    )
    
    print(f"Evaluation score: {result['evaluation'].score:.2f}")
    print(f"Recommendations: {result['evaluation'].recommendations}")

if __name__ == "__main__":
    main()
