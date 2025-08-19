import difflib 
 
def detect_hallucination_similarity(answer, correct_answers, threshold=0.5): 
    if not answer or not correct_answers: 
        return True 
    max_similarity = 0 
    for correct in correct_answers: 
        sim = difflib.SequenceMatcher(None, answer.lower(), str(correct).lower()).ratio() 
        max_similarity = max(max_similarity, sim) 
    return max_similarity < threshold 
 
print("=== Testing New Detection Logic ===") 
test_cases = [ 
    ("Paris", ["Paris"], False), 
    ("London", ["Paris"], True), 
    ("I think around 50 million", ["67 million"], True) 
] 
for answer, correct, expected in test_cases: 
    result = detect_hallucination_similarity(answer, correct, 0.5) 
    status = "?" if result == expected else "?" 
    print(f"Test: '{answer}' vs '{correct[0]}' Expected:{expected} Got:{result} {status}") 
