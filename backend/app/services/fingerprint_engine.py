import hashlib
from typing import Optional

class FingerprintEngine:
    """
    Generates deterministic fingerprints for alerts to enable deduplication and correlation.
    """
    
    def generate(self, service_id: str, rule_id: str, labels: Optional[dict] = None) -> str:
        """
        Creates a SHA-256 hash based on service, rule, and optional labels.
        """
        components = [service_id, rule_id]
        
        if labels:
            sorted_labels = sorted(labels.items())
            for k, v in sorted_labels:
                components.append(f"{k}:{v}")
                
        raw_fingerprint = "|".join(components)
        return hashlib.sha256(raw_fingerprint.encode("utf-8")).hexdigest()
