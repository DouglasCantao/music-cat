import aws_cdk as core
import aws_cdk.assertions as assertions

from music_categorization.music_categorization_stack import MusicCategorizationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in music_categorization/music_categorization_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MusicCategorizationStack(app, "music-categorization")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
