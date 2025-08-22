from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json

@dataclass
class AuditEntry:
    timestamp: datetime
    actor_id: str
    action: str
    input_hash: str
    output_hash: str
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        self.entry_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        data = {
            'timestamp': self.timestamp.isoformat(),
            'actor_id': self.actor_id,
            'action': self.action,
            'input_hash': self.input_hash,
            'output_hash': self.output_hash,
            'metadata': self.metadata
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

class AuditTrail:
    def __init__(self):
        self.entries: List[AuditEntry] = []
    
    def add_entry(self, actor_id: str, action: str, input_data: Any, output_data: Any, metadata: Dict[str, Any] = None) -> str:
        input_hash = self._hash_data(input_data)
        output_hash = self._hash_data(output_data)
        
        entry = AuditEntry(
            timestamp=datetime.now(),
            actor_id=actor_id,
            action=action,
            input_hash=input_hash,
            output_hash=output_hash,
            metadata=metadata or {}
        )
        
        self.entries.append(entry)
        return entry.entry_hash
    
    def _hash_data(self, data: Any) -> str:
        if isinstance(data, str):
            return hashlib.sha256(data.encode()).hexdigest()
        return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        for entry in self.entries:
            if entry.entry_hash != entry._compute_hash():
                return False
        return True
