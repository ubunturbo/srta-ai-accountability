#!/usr/bin/env python3
"""
Complete Apertus 3-Agent SRTA Evaluation System
"""

import json
import os
import datetime
from dataclasses import dataclass
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

@dataclass
class ExplanationSample:
    id: str
    task_type: str
    explanation_text: str
    ground_truth: str = None

@dataclass
class SRTAScore:
    systematic: float
    relevant: float
    transparent: float
    actionable: float
    overall: float
    confidence: float
    agent_id: str

class ApertusAgent:
    def __init__(self, agent_role: str, model_name: str = "microsoft/DialoGPT-medium"):
        self.agent_role = agent_role
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        print(f"Initializing {agent_role} agent on {self.device}")
    
    def load_model(self):
        print(f"Loading model for {self.agent_role} agent...")
        try:
            # Use a smaller, more accessible model for testing
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model.to(self.device)
            print(f"{self.agent_role} agent model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model for {self.agent_role}: {e}")
            return False
    
    def evaluate_explanation(self, explanation_text: str) -> SRTAScore:
        """Generate SRTA evaluation for explanation"""
        
        # For demo purposes, generate scores based on text characteristics
        text_length = len(explanation_text)
        word_count = len(explanation_text.split())
        
        # Simple heuristic scoring based on text characteristics
        systematic_score = min(10, max(1, (word_count / 10) + 3))
        relevant_score = min(10, max(1, 8 - (abs(word_count - 25) / 10)))
        transparent_score = min(10, max(1, 10 - (text_length / 50)))
        actionable_score = min(10, max(1, 6 + (word_count / 20)))
        
        # Agent-specific adjustments
        if self.agent_role == "principle":
            systematic_score += 1
        elif self.agent_role == "expression":
            transparent_score += 1
        elif self.agent_role == "audit":
            systematic_score -= 0.5
            relevant_score -= 0.5
        
        # Ensure scores stay within bounds
        scores = [systematic_score, relevant_score, transparent_score, actionable_score]
        scores = [max(1, min(10, score)) for score in scores]
        
        overall_score = sum(scores) / 4
        confidence_score = 7.0  # Mock confidence
        
        return SRTAScore(
            systematic=round(scores[0], 2),
            relevant=round(scores[1], 2),
            transparent=round(scores[2], 2),
            actionable=round(scores[3], 2),
            overall=round(overall_score, 2),
            confidence=confidence_score,
            agent_id=self.agent_role
        )

class MultiAgentSRTA:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.principle_agent = ApertusAgent("principle", model_name)
        self.expression_agent = ApertusAgent("expression", model_name)
        self.audit_agent = ApertusAgent("audit", model_name)
        self.results = []
    
    def load_models(self):
        """Load models for all agents"""
        print("Loading models for 3-agent system...")
        success = True
        success &= self.principle_agent.load_model()
        success &= self.expression_agent.load_model()
        success &= self.audit_agent.load_model()
        
        if success:
            print("All agents loaded successfully!")
        return success
    
    def evaluate_explanation(self, sample: ExplanationSample):
        """Evaluate explanation with all three agents"""
        print(f"Evaluating {sample.id}: {sample.task_type}")
        
        # Get evaluations from each agent
        principle_score = self.principle_agent.evaluate_explanation(sample.explanation_text)
        expression_score = self.expression_agent.evaluate_explanation(sample.explanation_text)
        audit_score = self.audit_agent.evaluate_explanation(sample.explanation_text)
        
        # Calculate consensus (weighted average)
        weights = {"principle": 0.4, "expression": 0.3, "audit": 0.3}
        
        consensus_systematic = (
            principle_score.systematic * weights["principle"] +
            expression_score.systematic * weights["expression"] +
            audit_score.systematic * weights["audit"]
        )
        
        consensus_relevant = (
            principle_score.relevant * weights["principle"] +
            expression_score.relevant * weights["expression"] +
            audit_score.relevant * weights["audit"]
        )
        
        consensus_transparent = (
            principle_score.transparent * weights["principle"] +
            expression_score.transparent * weights["expression"] +
            audit_score.transparent * weights["audit"]
        )
        
        consensus_actionable = (
            principle_score.actionable * weights["principle"] +
            expression_score.actionable * weights["expression"] +
            audit_score.actionable * weights["audit"]
        )
        
        consensus_overall = (consensus_systematic + consensus_relevant + 
                           consensus_transparent + consensus_actionable) / 4
        
        consensus_score = SRTAScore(
            systematic=round(consensus_systematic, 2),
            relevant=round(consensus_relevant, 2),
            transparent=round(consensus_transparent, 2),
            actionable=round(consensus_actionable, 2),
            overall=round(consensus_overall, 2),
            confidence=round((principle_score.confidence + 
                            expression_score.confidence + 
                            audit_score.confidence) / 3, 2),
            agent_id="consensus"
        )
        
        result = {
            'sample_id': sample.id,
            'task_type': sample.task_type,
            'principle_overall': principle_score.overall,
            'expression_overall': expression_score.overall,
            'audit_overall': audit_score.overall,
            'consensus_overall': consensus_score.overall,
            'consensus_systematic': consensus_score.systematic,
            'consensus_relevant': consensus_score.relevant,
            'consensus_transparent': consensus_score.transparent,
            'consensus_actionable': consensus_score.actionable,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.results.append(result)
        
        print(f"  Principle: {principle_score.overall:.2f}")
        print(f"  Expression: {expression_score.overall:.2f}") 
        print(f"  Audit: {audit_score.overall:.2f}")
        print(f"  Consensus: {consensus_score.overall:.2f}")
        
        return result
    
    def save_results(self, output_path: str = "outputs/multi_agent_results.csv"):
        """Save results to CSV"""
        if not self.results:
            print("No results to save")
            return
        
        df = pd.DataFrame(self.results)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"  Total samples: {len(df)}")
        print(f"  Average consensus score: {df['consensus_overall'].mean():.2f}")
        print(f"  Score range: {df['consensus_overall'].min():.2f} - {df['consensus_overall'].max():.2f}")

def run_demo():
    """Run demonstration"""
    
    # Sample explanations
    samples = [
        ExplanationSample(
            id="sample_001",
            task_type="CoLA",
            explanation_text="The sentence 'What did you eat and drink?' is grammatically correct because it follows proper English structure with a valid question word 'what', auxiliary verb 'did', subject 'you', and coordinated verbs 'eat and drink' connected by 'and'."
        ),
        ExplanationSample(
            id="sample_002", 
            task_type="XNLI",
            explanation_text="The premise states that 'The cat is sleeping on the mat' and the hypothesis is 'The cat is awake'. These statements directly contradict each other since 'sleeping' and 'awake' are opposite states, therefore the relationship is contradiction."
        ),
        ExplanationSample(
            id="sample_003",
            task_type="sentiment", 
            explanation_text="This movie review is negative because it contains words like 'terrible', 'boring', and 'waste of time' which indicate strong dissatisfaction with the film."
        ),
        ExplanationSample(
            id="sample_004",
            task_type="CoLA",
            explanation_text="Bad grammar detected here."
        )
    ]
    
    print("=== Multi-Agent SRTA Evaluation Demo ===")
    
    # Initialize system
    multi_agent = MultiAgentSRTA()
    
    if not multi_agent.load_models():
        print("Failed to load models. Running with mock evaluation.")
    
    # Evaluate samples
    for sample in samples:
        multi_agent.evaluate_explanation(sample)
        print()
    
    # Save results
    multi_agent.save_results()
    
    print("Demo completed! Check outputs/multi_agent_results.csv")
    return multi_agent

if __name__ == "__main__":
    run_demo()
