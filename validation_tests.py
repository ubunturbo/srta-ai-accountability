def validate_compliance_scores(scores):
    """Ensure all compliance scores are in valid range [0, 1.0]"""
    for framework, score in scores.items():
        assert 0.0 <= score <= 1.0, f"{framework} score {score} outside valid range"
    return True

def validate_explanation_completeness(report):
    """Verify explanation addresses required questions"""
    required = ['what', 'why', 'how', 'who']
    for question in required:
        assert hasattr(report, question), f"Missing {question} in explanation"
        assert getattr(report, question), f"Empty {question} field"
    return True
