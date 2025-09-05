import re
from collections import Counter

def tokenize_simple(text: str):
    return re.findall(r'\b\w+\b', text.lower())

def word_overlap_score(text1: str, text2: str) -> float:
    """Calculate word overlap using token frequency"""
    tokens1 = tokenize_simple(text1)
    tokens2 = tokenize_simple(text2)
    
    if not tokens1 or not tokens2:
        return 0.0
    
    # Use word frequency for better matching
    freq1 = Counter(tokens1)
    freq2 = Counter(tokens2)
    
    # Calculate intersection based on minimum frequencies
    common_words = set(freq1.keys()) & set(freq2.keys())
    intersection_score = sum(min(freq1[word], freq2[word]) for word in common_words)
    
    # Normalize by average length
    avg_length = (len(tokens1) + len(tokens2)) / 2
    return intersection_score / avg_length if avg_length > 0 else 0.0

def bigram_jaccard(text1: str, text2: str) -> float:
    """Calculate bigram Jaccard similarity"""
    tokens1 = tokenize_simple(text1)
    tokens2 = tokenize_simple(text2)
    
    if len(tokens1) < 2 or len(tokens2) < 2:
        return word_overlap_score(text1, text2)  # Fallback to word overlap
    
    bigrams1 = set(tuple(tokens1[i:i+2]) for i in range(len(tokens1) - 1))
    bigrams2 = set(tuple(tokens2[i:i+2]) for i in range(len(tokens2) - 1))
    
    intersection = len(bigrams1 & bigrams2)
    union = len(bigrams1 | bigrams2)
    
    return intersection / union if union > 0 else 0.0

def improved_similarity(text1: str, text2: str) -> float:
    """Improved similarity combining word overlap and bigrams"""
    word_score = word_overlap_score(text1, text2)
    bigram_score = bigram_jaccard(text1, text2)
    
    # Weighted combination: favor word overlap for robustness
    return 0.7 * word_score + 0.3 * bigram_score

# Test all methods
text1 = "The capital of France is Paris."
text2 = "Paris is the capital and most populous city of France."

print("Improved Attribution Testing")
print("=" * 35)
print(f"Text1: {text1}")
print(f"Text2: {text2}")
print()

word_score = word_overlap_score(text1, text2)
bigram_score = bigram_jaccard(text1, text2)
final_score = improved_similarity(text1, text2)

print(f"Word overlap score: {word_score:.3f}")
print(f"Bigram Jaccard score: {bigram_score:.3f}")
print(f"Combined score: {final_score:.3f}")

# Test with poor match
text3 = "The weather will be sunny tomorrow."
poor_score = improved_similarity(text3, text2)
print(f"\nPoor match score: {poor_score:.3f}")
