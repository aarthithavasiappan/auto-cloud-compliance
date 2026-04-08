from abc import ABC, abstractmethod
from typing import List
from .models import Resource, Finding, Severity

class ComplianceRule(ABC):
    
    @property
    @abstractmethod
    def rule_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def severity(self) -> Severity:
        pass
        
    @abstractmethod
    def evaluate(self, resource: Resource) -> List[Finding]:
        """Evaluates a resource against the rule. Returns a list of findings."""
        pass
