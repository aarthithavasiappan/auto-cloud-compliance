from typing import Dict, Any
from cspm.remediation.actions import REMEDIATION_MAP

class RemediationOrchestrator:
    def __init__(self, ai_threshold: int = 85):
        # Only auto-remediate if AI score is above this threshold
        self.ai_threshold = ai_threshold
        
    def process_finding(self, finding_data: Dict[str, Any]) -> str:
        if finding_data.get("is_compliant"):
            return "SKIPPED_COMPLIANT"
            
        ai_eval = finding_data.get("ai_evaluation", {})
        score = ai_eval.get("ai_risk_score", 0)
        
        remediation_id = finding_data.get("remediation_action")
        resource_id = finding_data.get("resource_id")
        account_id = finding_data.get("account_id")
        
        if score >= self.ai_threshold:
            print(f"   [*] High Risk Detected (Score: {score}). Initiating Remediation Workflow...")
            action_func = REMEDIATION_MAP.get(remediation_id)
            if action_func:
                success = action_func(resource_id, account_id)
                return "AUTO_REMEDIATED" if success else "MANUAL_INTERVENTION_REQUIRED"
            else:
                print(f"   [!] No automated playbook found for action '{remediation_id}'.")
                return "NO_PLAYBOOK"
        elif score > 0:
            print(f"   [-] Low/Medium Risk (Score: {score}). Threshold {self.ai_threshold} not met. Creating security ticket...")
            return "TICKETED"
            
        return "UNKNOWN"
