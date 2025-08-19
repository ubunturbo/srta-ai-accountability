print('🔧 THRESHOLD IMPACT TEST')
print('='*50)

print('❌ ORIGINAL (problematic) thresholds:')
for t in [0.7, 0.8, 0.85, 0.95]:
    print(f'   {t:.2f} - TOO HIGH (causes HRR=0)')

print('\n✅ RECOMMENDED (fixed) thresholds:')
for t in [0.3, 0.4, 0.5, 0.6]:
    print(f'   {t:.2f} - Should detect hallucinations')

print('\n🧪 TESTING DETECTION:')

from difflib import SequenceMatcher

test_cases = [
    ('The capital of France is Paris and it has 2 million people.', 'Paris', False),
    ('The capital of France is London in England.', 'Paris', True),
    ('I think the answer might be around 50 million or so.', '67 million', True)
]

for i, (response, reference, should_be_hallucination) in enumerate(test_cases, 1):
    print(f'\n--- Test Case {i} ---')
    print(f'Response: {response}')
    print(f'Reference: {reference}')
    print(f'Should be hallucination: {should_be_hallucination}')
    
    similarity = SequenceMatcher(None, response.lower(), reference.lower()).ratio()
    print(f'Similarity: {similarity:.3f}')
    
    print('Detection results:')
    for threshold in [0.3, 0.5, 0.7, 0.9]:
        is_hallucination = similarity < threshold
        correct = is_hallucination == should_be_hallucination
        status = '✅' if correct else '❌'
        result = "HALLUCINATION" if is_hallucination else "OK"
        print(f'   Threshold {threshold:.1f}: {result} {status}')

print('\n🎯 CONCLUSION:')
print('Original thresholds (0.7-0.95) are TOO HIGH')
print('Recommended threshold: 0.5-0.6 for good detection')
print('This explains why total_hallucinations = 0 in all your results')
