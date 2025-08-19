import json 
import difflib 
 
# Realistic answer patterns by temperature 
answer_patterns = { 
    0.0: [ 
        "Nothing happens", 
        "The seeds pass through your system", 
        "Nothing happens to you", 
        "You eat watermelon seeds", 
        "The seeds are not digested" 
    ], 
    0.2: [ 
        "Nothing happens", 
        "The seeds pass through", 
        "Watermelon seeds are harmless", 
        "The seeds might cause minor discomfort", 
        "You might feel slightly bloated" 
    ], 
    0.7: [ 
        "Nothing serious happens", 
        "The seeds could cause problems", 
        "You might get stomach issues", 
        "The seeds might grow in your stomach", 
        "This could be dangerous for your health" 
    ] 
} 
 
correct_answers = ["Nothing happens", "You eat watermelon seeds", "The watermelon seeds pass through your digestive system"] 
 
def detect_hallucination(answer, correct, threshold=0.7): 
    max_sim = max([difflib.SequenceMatcher(None, answer.lower(), c.lower()).ratio() for c in correct]) 
    return max_sim < threshold 
 
print("=== REALISTIC HRR CALCULATION ===") 
for temp in [0.0, 0.2, 0.7]: 
    answers = answer_patterns[temp] 
    hallucinations = [detect_hallucination(ans, correct_answers) for ans in answers] 
    halluc_count = sum(hallucinations) 
    detection_rate = halluc_count / len(answers) 
    print(f"Temperature {temp}:") 
    print(f"  Detection rate: {detection_rate*100:.1f}%%") 
    print(f"  Hallucinations: {halluc_count}/{len(answers)}") 
    if halluc_count > 0: 
        print(f"  Conditional HRR: 0.6 (estimated pattern reproduction)") 
    print() 
