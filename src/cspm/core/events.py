from typing import Dict, Any, Optional
from .models import Resource
import json

def parse_config_event(event: Dict[str, Any]) -> Optional[Resource]:
    """Parses an EventBridge event corresponding to an AWS Config item change."""
    if event.get("source") != "aws.config":
        return None
        
    detail = event.get("detail", {})
    configuration_item = detail.get("configurationItem", {})
    
    resource_type = configuration_item.get("resourceType")
    resource_id = configuration_item.get("resourceId")
    account_id = configuration_item.get("accountId")
    region = configuration_item.get("awsRegion")
    configuration = configuration_item.get("configuration", {})
    tags = configuration_item.get("tags", {})
    
    if not resource_type or not resource_id:
        return None
        
    # If the payload came as a string (happens in some events), decode it
    if isinstance(configuration, str):
        try:
            configuration = json.loads(configuration)
        except json.JSONDecodeError:
            configuration = {}
            
    return Resource(
        id=resource_id,
        resource_type=resource_type,
        region=region,
        account_id=account_id,
        configuration=configuration,
        tags=tags
    )
