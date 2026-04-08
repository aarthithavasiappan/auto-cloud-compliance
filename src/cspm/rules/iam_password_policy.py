from cspm.core.rule import ComplianceRule
from cspm.core.models import Resource, Finding, Severity
from typing import List

class IAMPasswordPolicyRule(ComplianceRule):
    @property
    def rule_id(self) -> str:
        return "CIS-1.14"
        
    @property
    def title(self) -> str:
        return "Ensure hardware MFA is enabled for the 'root' account"
        
    @property
    def severity(self) -> Severity:
        return Severity.CRITICAL
        
    def evaluate(self, resource: Resource) -> List[Finding]:
        if resource.resource_type != "AWS::IAM::AccountSummary":
            return []
            
        config = resource.configuration
        
        # In a real environment, we check the AccountSummary
        mfa_active = config.get("AccountMFAEnabled", False)
        
        finding = Finding(
            rule_id=self.rule_id,
            title=self.title,
            description=f"Root account MFA is {'enabled' if mfa_active else 'disabled'}.",
            severity=self.severity,
            resource_id=resource.id,
            account_id=resource.account_id,
            region=resource.region,
            is_compliant=mfa_active,
            remediation_action="iam:EnableMFADevice" if not mfa_active else ""
        )
        
        return [finding]
