from typing import List
from cspm.core.models import Resource

def get_mock_resources() -> List[Resource]:
    return [
        # Non-compliant S3 Bucket
        Resource(
            id="my-public-company-data-bucket",
            resource_type="AWS::S3::Bucket",
            region="us-east-1",
            account_id="123456789012",
            configuration={
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": False,
                    "IgnorePublicAcls": False,
                    "BlockPublicPolicy": False,
                    "RestrictPublicBuckets": False
                }
            },
            tags={"Environment": "Production", "DataClassification": "Confidential"}
        ),
        # Compliant S3 Bucket
        Resource(
            id="my-secure-log-bucket",
            resource_type="AWS::S3::Bucket",
            region="us-east-1",
            account_id="123456789012",
            configuration={
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True
                }
            },
            tags={"Environment": "Development"}
        ),
        # Non-compliant IAM Account Summary
        Resource(
            id="aws-account-summary",
            resource_type="AWS::IAM::AccountSummary",
            region="global",
            account_id="123456789012",
            configuration={
                "AccountMFAEnabled": False
            }
        )
    ]
