import re

def tokenize_simple(text: str):
    return re.findall(r'\b\w+\b', text.lower())

def fuzzy_ngram_match(text1: str, text2: str, n: int = 3):
    tokens1 = tokenize_simple(text1)
    tokens2 = tokenize_simple(text2)
    
    print(f"Tokens1: {tokens1}")
    print(f"Tokens2: {tokens2}")
    
    if not tokens1 or not tokens2:
        return 0.0
    
    ngrams1 = set(' '.join(tokens1[i:i+n]) for i in range(len(tokens1) - n + 1))
    ngrams2 = set(' '.join(tokens2[i:i+n]) for i in range(len(tokens2) - n + 1))
    
    print(f"N-grams1: {ngrams1}")
    print(f"N-grams2: {ngrams2}")
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    print(f"Intersection: {intersection}, Union: {union}")
    
    return intersection / union if union > 0 else 0.0

# Test the problematic case
text1 = "The capital of France is Paris."
text2 = "Paris is the capital and most populous city of France."

print("Debug Attribution Algorithm")
print("=" * 30)
score = fuzzy_ngram_match(text1, text2)
print(f"Final score: {score}")
