import re
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class SafetyFilter:
    """
    Native Python Guardrails blocking irrelevant, dangerous, or medical queries.
    This acts as Layer 1 in our Tri-Layer Guard pipeline.
    """
    
    # Heuristic dictionary compiled into a regex pattern for zero-latency scanning
    MEDICAL_AND_HARMFUL_TERMS = [
        r'\bdoctor\b', r'\bprescription\b', r'\bhospital\b', r'\bdiagnose me\b', 
        r'\bsurgery\b', r'\bcancer\b', r'\bheart attack\b', r'\bcovid\b',
        r'\bignore\s+(all\s+)?previous\s+instructions\b', r'\bbomb\b', r'\bterrorist\b',
        r'\bvote\b', r'\B#election\B', r'\bpresident\b'
    ]
    
    # Pre-compile the regex for maximum speed
    PATTERN = re.compile('|'.join(MEDICAL_AND_HARMFUL_TERMS), re.IGNORECASE)

    @classmethod
    def analyze(cls, text: str) -> None:
        """
        Scans input string against heuristic blocks.
        Raises HTTPException(422) if a blocked pattern is found.
        """
        if not text:
            return
            
        match = cls.PATTERN.search(text)
        if match:
            logger.warning(f"Guardrail triggered on keyword: {match.group(0)}")
            raise HTTPException(
                status_code=422,
                detail="I am an agricultural assistant and cannot respond to queries outside of farming, crop diagnosis, or agricultural markets."
            )

# Instantiate a singleton for easy import
guardrail = SafetyFilter()
