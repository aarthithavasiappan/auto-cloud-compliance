from cspm.core.rule import ComplianceRule
from cspm.core.models import Resource, Finding, Severity
from typing import List

class S3BlockPublicAccessRule(ComplianceRule):
    @property
    def rule_id(self) -> str:
        return "CIS-2.1.5"
        
    @property
    def title(self) -> str:
        return "Ensure that S3 Buckets are configured with 'Block public access (bucket settings)'"
        
    @property
    def severity(self) -> Severity:
        return Severity.HIGH
        
    def evaluate(self, resource: Resource) -> List[Finding]:
        if resource.resource_type != "AWS::S3::Bucket":
            return []
            
        config = resource.configuration
        public_access_block = config.get("PublicAccessBlockConfiguration", {})
        
        is_compliant = (
            public_access_block.get("BlockPublicAcls", False) and
            public_access_block.get("IgnorePublicAcls", False) and
            public_access_block.get("BlockPublicPolicy", False) and
            public_access_block.get("RestrictPublicBuckets", False)
        )
        
        finding = Finding(
            rule_id=self.rule_id,
            title=self.title,
            description=f"S3 bucket {resource.id} public access block is {'enabled' if is_compliant else 'disabled'}.",
            severity=self.severity,
            resource_id=resource.id,
            account_id=resource.account_id,
            region=resource.region,
            is_compliant=is_compliant,
            remediation_action="s3:PutPublicAccessBlock" if not is_compliant else ""
        )
        
        return [finding]
