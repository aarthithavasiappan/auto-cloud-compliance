import json
from cspm.core.scanner import Scanner
from cspm.rules.s3_public_access import S3BlockPublicAccessRule
from cspm.rules.iam_password_policy import IAMPasswordPolicyRule
from cspm.tests.mock_data import get_mock_resources
from dataclasses import asdict

def main():
    print("Initializing CSPM Scanner...")
    scanner = Scanner()
    
    # Register Rules
    scanner.register_rule(S3BlockPublicAccessRule())
    scanner.register_rule(IAMPasswordPolicyRule())
    
    # Load Mock Data
    print("Loading mock resources...")
    resources = get_mock_resources()
    
    # Scan Resources
    print(f"Scanning {len(resources)} resources...")
    findings = scanner.scan_resources(resources)
    
    # Output Findings
    print(f"\nScan Complete. Found {len(findings)} events. Results:")
    
    # Initialize AI Scorer and Orchestrator
    print("Initializing AI Scorer and Remediation Orchestrator...")
    from cspm.ai.gemini_scorer import AIRiskScorer
    from cspm.remediation.orchestrator import RemediationOrchestrator
    
    ai_scorer = AIRiskScorer()
    orchestrator = RemediationOrchestrator(ai_threshold=85)
    
    scored_findings = []
    
    for finding in findings:
        status_icon = "[PASS]" if finding.is_compliant else "[FAIL]"
        print(f"\n{status_icon} [{finding.severity.name}] {finding.rule_id} - {finding.title}")
        print(f"   Resource: {finding.resource_id} | Account: {finding.account_id}")
        
        # Find the original resource to pass to the AI
        resource = next((r for r in resources if r.id == finding.resource_id), None)
        
        if not finding.is_compliant and resource:
            ai_evaluation = ai_scorer.score_finding(finding, resource)
            score = ai_evaluation.get("ai_risk_score", 0)
            rationale = ai_evaluation.get("ai_rationale", "")
            
            print(f"   Required Remediation Action: {finding.remediation_action}")
            print(f"   [AI] Risk Score: {score}/100")
            print(f"   [AI] Rationale: {rationale}")
            
            scored_output = {**asdict(finding), "severity": finding.severity.name, "ai_evaluation": ai_evaluation}
            
            # Pass to orchestrator
            outcome = orchestrator.process_finding(scored_output)
            scored_output["remediation_outcome"] = outcome
        else:
            scored_output = {**asdict(finding), "severity": finding.severity.name}
            
        scored_findings.append(scored_output)

    # Save findings to output.json for downstream AI processing
    with open("findings.json", "w") as f:
        json.dump(scored_findings, f, indent=2)
    print("\nFindings exported to findings.json")

if __name__ == "__main__":
    main()
