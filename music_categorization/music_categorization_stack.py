from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    RemovalPolicy
)
from constructs import Construct

class MusicCategorizationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create the S3 Bucket with EventBridge enabled
        source_bucket = s3.Bucket(
            self, "IncomingFilesBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,  # Automatically delete objects on `cdk destroy`
            event_bridge_enabled=True
        )

        # 2. Create the Lambda Function
        # The IAM role will be automatically created by the CDK with the necessary
        # basic execution permissions.
        processor_lambda = _lambda.Function(
            self, "FileProcessorHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="file_handler.s3_file_handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        # 3. Grant the Lambda permission to read from the S3 bucket
        # This is the idiomatic CDK way to grant permissions. It adds the
        # necessary policies to the Lambda's execution role.
        source_bucket.grant_read(processor_lambda)

        # 4. Create an EventBridge Rule to trigger the Lambda
        s3_event_rule = events.Rule(
            self, "S3UploadRule",
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["Object Created"],
                detail={
                    "bucket": {
                        "name": [source_bucket.bucket_name]
                    }
                }
            )
        )

        # 5. Set the Lambda function as the target for the EventBridge rule
        s3_event_rule.add_target(targets.LambdaFunction(processor_lambda))