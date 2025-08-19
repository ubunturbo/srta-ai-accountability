from datasets import load_dataset 
print("Loading TruthfulQA dataset...") 
dataset = load_dataset('truthful_qa', 'generation', split='validation') 
sample = dataset[0] 
print("Sample data structure:") 
print("- Question:", sample['question'][:100]) 
print("- Correct answers:", sample['correct_answers']) 
print("- Has incorrect_answers:", 'incorrect_answers' in sample) 
if 'incorrect_answers' in sample: 
    print("- Incorrect answers count:", len(sample['incorrect_answers'])) 
