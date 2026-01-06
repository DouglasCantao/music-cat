from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    RemovalPolicy
)
from constructs import Construct

class MusicCategorizationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create the S3 Bucket
        # We must enable 'event_bridge_enabled' for S3 to send events to the bus
        source_bucket = s3.Bucket(
            self, "IncomingFilesBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY, # Only for dev/testing
            auto_delete_objects=False,            # Only for dev/testing
            event_bridge_enabled=True            # Critical step!
        )

        # 2a. Create an IAM Role for the Lambda
        # lambda_role = iam.Role(
        #     self, "FileProcessorRole",
        #     assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        # )
        # lambda_role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        # )

        # 1. Define the IAM Role
        lambda_role = iam.Role(self, "LambdaS3ExecutionRole",
            # Trust policy: allows the Lambda service to use this role
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            # Add basic logging permissions (recommended)
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # 2. Add an inline policy to the role for S3 access
        lambda_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:GetObject", "s3:ListBucket"],
            resources=[
                source_bucket.bucket_arn,          # Permission for the bucket itself
            ]
        ))

        # 2b. Create the Lambda Function
        processor_lambda = _lambda.Function(
            self, "FileProcessorHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="file_handler.s3_file_handler",
            code=_lambda.Code.from_asset("lambda"),
            role=lambda_role  # Assign the role here
        )

        # 3. Grant the Lambda permission to read from the bucket
        source_bucket.grant_read(processor_lambda)

        # 4. Create an EventBridge Rule
        # This rule listens for "Object Created" events from our specific bucket
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

        # 5. Add the Lambda as the target for the EventBridge Rule
        s3_event_rule.add_target(targets.LambdaFunction(processor_lambda))