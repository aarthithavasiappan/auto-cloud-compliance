from cspm.handlers.event_consumer import lambda_handler

test_event = {
    "version": "0",
    "id": "12345678-1234-1234-1234-123456789012",
    "detail-type": "Config Configuration Item Change",
    "source": "aws.config",
    "account": "123456789012",
    "time": "2026-04-08T08:00:00Z",
    "region": "us-east-1",
    "resources": [
        "arn:aws:s3:::my-public-company-data-bucket"
    ],
    "detail": {
        "configurationItem": {
            "resourceType": "AWS::S3::Bucket",
            "resourceId": "my-public-company-data-bucket",
            "accountId": "123456789012",
            "awsRegion": "us-east-1",
            "configuration": {
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": False,
                    "IgnorePublicAcls": False,
                    "BlockPublicPolicy": False,
                    "RestrictPublicBuckets": False
                }
            },
            "tags": {"Environment": "Production"}
        }
    }
}

if __name__ == "__main__":
    print("Testing Lambda Handler with Mock EventBridge Event...")
    result = lambda_handler(test_event, None)
    print(f"Result: {result}")
