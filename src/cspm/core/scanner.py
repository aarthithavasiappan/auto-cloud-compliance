from typing import List
from .models import Resource, Finding
from .rule import ComplianceRule

class Scanner:
    def __init__(self):
        self.rules: List[ComplianceRule] = []
        
    def register_rule(self, rule: ComplianceRule):
        self.rules.append(rule)
        
    def scan_resource(self, resource: Resource) -> List[Finding]:
        findings = []
        for rule in self.rules:
            findings.extend(rule.evaluate(resource))
        return findings
    
    def scan_resources(self, resources: List[Resource]) -> List[Finding]:
        findings = []
        for resource in resources:
            findings.extend(self.scan_resource(resource))
        return findings
