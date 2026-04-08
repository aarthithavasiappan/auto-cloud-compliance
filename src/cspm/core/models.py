from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

@dataclass
class Resource:
    id: str
    resource_type: str
    region: str
    account_id: str
    configuration: Dict[str, Any]
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class Finding:
    rule_id: str
    title: str
    description: str
    severity: Severity
    resource_id: str
    account_id: str
    region: str
    is_compliant: bool
    remediation_action: str = ""
