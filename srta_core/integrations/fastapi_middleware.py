"""FastAPI Middleware Integration - Simplified"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Fix import path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir / "governance"))

from governance_core import GovernanceCore, Policy, Action

class GovernanceRequest(BaseModel):
    prompt: str
    output: str
    signals: Optional[Dict[str, float]] = {}

def create_demo_app():
    app = FastAPI(title="SRTA Governance Demo")
    
    # Simple policies for demo
    policies = [
        Policy(id="DEMO_SAFETY", owner="Safety", signal="toxicity", 
               operator="<", threshold=0.3, severity="block", weight=2.0),
        Policy(id="DEMO_QUALITY", owner="Quality", signal="confidence",
               operator=">", threshold=0.5, severity="warn", weight=1.0)
    ]
    
    governance = GovernanceCore(policies=policies, actors=["Safety", "Quality", "Operations"])
    
    @app.post("/evaluate")
    async def evaluate_content(request: GovernanceRequest):
        """Evaluate content with governance"""
        
        # Auto-compute missing signals
        signals = dict(request.signals)
        if "toxicity" not in signals:
            toxic_words = ['hate', 'kill', 'violence']
            signals["toxicity"] = sum(1 for word in toxic_words if word in request.output.lower()) / 10.0
        if "confidence" not in signals:
            signals["confidence"] = 0.8 if len(request.output) > 10 else 0.4
        
        rtr = governance.evaluate(
            prompt=request.prompt,
            output=request.output,
            signals=signals
        )
        
        if rtr.action == Action.BLOCK:
            raise HTTPException(status_code=403, detail={
                "error": "Content blocked",
                "reason": rtr.reason,
                "audit_id": rtr.decision_id
            })
        
        return {
            "content": request.output,
            "action": rtr.action.value,
            "reason": rtr.reason,
            "responsibility": rtr.responsibility,
            "audit_id": rtr.decision_id,
            "review_required": rtr.action == Action.REVIEW
        }
    
    @app.get("/")
    async def root():
        return {"message": "SRTA Governance API Demo"}
    
    return app

if __name__ == "__main__":
    import uvicorn
    app = create_demo_app()
    print("Starting SRTA Governance API on http://localhost:8000")
    print("Test with: POST /evaluate")
    uvicorn.run(app, host="127.0.0.1", port=8000)
