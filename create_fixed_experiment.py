# Create fixed version with similarity-based detection 
import re 
 
with open('experiments/hallucination_reproduction.py', 'r', encoding='utf-8') as f: 
    content = f.read() 
 
# New detection function 
    import difflib 
    if not answer or not correct_answers: 
        return True 
    max_similarity = 0 
    for correct in correct_answers: 
        sim = difflib.SequenceMatcher(None, answer.lower(), str(correct).lower()).ratio() 
        max_similarity = max(max_similarity, sim) 
    return max_similarity < threshold 
 
 
# Insert new function before detect_span 
content = content.replace('def detect_span', new_function + '\ndef detect_span') 
 
# Replace the detection call 
content = content.replace('sp=detect_span(ans, incorrect)', 'sp="hallucination" if detect_hallucination_similarity(ans, ex.get("correct_answers", []), 0.5) else None') 
 
# Save the fixed version 
with open('experiments/hallucination_reproduction_fixed.py', 'w', encoding='utf-8') as f: 
    f.write(content) 
 
print("? Fixed version created successfully!") 
print("Now run: python experiments/hallucination_reproduction_fixed.py") 
