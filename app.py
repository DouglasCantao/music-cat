#!/usr/bin/env python3
import os

import aws_cdk as cdk

from music_categorization.music_categorization_stack import MusicCategorizationStack


app = cdk.App()
MusicCategorizationStack(app, "MusicCategorizationStack",

    # For now, a single stack in 'default' account/region
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
