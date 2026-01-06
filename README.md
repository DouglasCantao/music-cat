# AWS CLI First Login and CDK Setup Guide

## Simple Resource Check

To check if you're logged in, run:

```bash
aws s3 ls
```

If not logged in, you'll see:
```
Unable to locate credentials. You can configure credentials by running "aws login or configure".
```

## First Time Setup

### Prerequisites

1. Create your IAM user
2. Set the keys for this user

### Configure AWS CLI

#### Default Profile

To create a default profile, run:

```bash
aws configure
```

You'll be prompted for:
- **AWS Access Key ID**: `<user-key>`
- **AWS Secret Access Key**: `<user-secret>`
- **Default region name**: `<region>` (e.g., `us-west-2`)
- **Default output format**: (can keep blank)

#### Named Profile

To add a named profile, run:

```bash
aws configure --profile <profile-name>
```

### List Profiles

To list all configured profiles:

```bash
aws configure list-profiles
```

### List Resources

To list S3 resources:

```bash
aws s3 ls
```

Or for a specific profile:

```bash
aws s3 ls --profile <profile-name>
```

## AWS CDK Python Project Setup

### Initialize CDK Project

To initialize a new CDK Python project:

```bash
cdk init app --language python
```

### Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization process also creates a virtualenv within this project, stored under the `.venv` directory. To create the virtualenv it assumes that there is a `python3` (or `python` for Windows) executable in your path with access to the `venv` package. If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv manually.

#### Manual Virtualenv Creation

**MacOS and Linux:**

```bash
python3 -m venv .venv
```

**MacOS and Linux:**

```bash
source .venv/bin/activate
```

#### Install Dependencies

Once the virtualenv is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

#### Add Additional Dependencies

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun:

```bash
pip install -r requirements.txt
```

### Useful CDK Commands

- `cdk ls` - list all stacks in the app
- `cdk synth` - emits the synthesized CloudFormation template
- `cdk deploy` - deploy this stack to your default AWS account/region
- `cdk diff` - compare deployed stack with current state
- `cdk docs` - open CDK documentation

## AWS Account Information

### Get AWS Account ID

Run the following AWS CLI command to get the AWS Account ID for your default profile:

```bash
aws sts get-caller-identity --query "Account" --output text
```

### Get AWS Region

Run the following AWS CLI command to get the AWS Region for your default profile:

```bash
aws configure get region
```

## CDK Operations

### Bootstrap Environment

To bootstrap your environment, run the following command from the root of your AWS CDK project:

```bash
cdk bootstrap
```

### Synthesize CloudFormation Template

To synthesize a CloudFormation template, run the following from the root of your project:

```bash
cdk synth
```

### Deploy CDK Stack

From the root of your project, run the following. Confirm changes if prompted:

```bash
cdk deploy
```

### Destroy CDK Stack

To destroy the stack, run the following from the root of your project. Confirm changes if prompted:

```bash
cdk destroy
```

