from typing import Dict, Any
from cspm.core.events import parse_config_event
from cspm.core.scanner import Scanner
from cspm.rules.s3_public_access import S3BlockPublicAccessRule
from cspm.rules.iam_password_policy import IAMPasswordPolicyRule

scanner = Scanner()
scanner.register_rule(S3BlockPublicAccessRule())
scanner.register_rule(IAMPasswordPolicyRule())

def lambda_handler(event: Dict[str, Any], context: Any):
    """Entry point for the AWS Lambda event consumer."""
    print(f"Received Event: {event.get('id', 'Unknown')}")
    
    resource = parse_config_event(event)
    if not resource:
        print("Ignored non-Config event or invalid format.")
        return {"statusCode": 200, "body": "Ignored"}
        
    findings = scanner.scan_resource(resource)
    
    # In a real environment, store findings to DynamoDB or trigger remediation
    for finding in findings:
        status = "COMPLIANT" if finding.is_compliant else "NON_COMPLIANT"
        print(f"[{status}] Rule: {finding.rule_id} against Resource: {finding.resource_id}")
        
    return {"statusCode": 200, "findings": len(findings)}
