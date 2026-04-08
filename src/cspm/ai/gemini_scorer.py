import os
import json
from dataclasses import asdict
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

from cspm.core.models import Finding, Resource

class AIRiskScorer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key:
            genai.configure(api_key=self.api_key)
            # using default general model as an example
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def _generate_prompt(self, finding: Finding, resource: Resource) -> str:
        prompt = f"""
You are an expert Cloud Security Posture Management (CSPM) AI. Review the following security finding and resource context, and evaluate the true risk.

Finding Rule: {finding.rule_id} - {finding.title}
Severity baseline: {finding.severity.name}
Resource ID: {resource.id}
Resource Tags: {resource.tags}
Configuration: {json.dumps(resource.configuration)[:500]} 

Instructions:
1. Provide a score from 1-100 representing the risk severity (100 is critical immediate risk).
2. Consider context like "Production" tags or whether it's external facing. If tags read "Development", lower the score.
3. Respond strictly in valid JSON format with standard keys: "ai_risk_score" (int) and "ai_rationale" (string).
"""
        return prompt

    def score_finding(self, finding: Finding, resource: Resource) -> dict:
        if finding.is_compliant:
            return {"ai_risk_score": 0, "ai_rationale": "Resource is compliant."}

        if not self.model:
            # Fallback mock logic when API key or package is missing
            score = 95 if finding.severity.name == "CRITICAL" else 75
            if "Production" in resource.tags.values():
                score += 5
            elif "Development" in resource.tags.values():
                score -= 40
            score = min(100, max(1, score))
            return {
                "ai_risk_score": score,
                "ai_rationale": f"[MOCK] AI assessed base severity {finding.severity.name}. Scored {score} based on context tags: {resource.tags}"
            }

        prompt = self._generate_prompt(finding, resource)
        try:
            response = self.model.generate_content(prompt)
            # Expecting response.text to be JSON string
            text_resp = response.text.strip()
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:-3]
            elif text_resp.startswith("```"):
                text_resp = text_resp[3:-3]
            return json.loads(text_resp)
        except Exception as e:
            return {
                "ai_risk_score": 50,
                "ai_rationale": f"AI Scoring failed: {str(e)}"
            }
