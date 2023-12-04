## Overview
CodersConduit template package for creating Lambda functions in AWS.  
Best used in conjunction with the [CodersConduit Base CDK Template](https://github.com/CodersConduit/cdk-base-template).


## Contents

#### Lambda Handler `lambda_function.lambda_handler`
> This is the Lambda functions entry point and must be specified when creating the Lambda, either from CDK, CLI or elsewhere.  
> Accepts args `event`, `context`.  
>
> <small>*For more info on lambda handlers or the `event`/`context` arguments see the [Official AWS Python Lambda Handler Documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html).*</small>

#### CodersConduit Custom Build tool - ccbuild.py
> This is a custom build tool designed to easily integrate lambda functions with the base cdk template.  
> 
> When executed, this tool will run unit tests, perform a basic build of the project, and assuming successful build and tests will create the lambda zip file under the `ccbuild/` directory.
 
#### Lambda Build Config
> Located under `config/build_config`, this contains some useful configurations that are used to build the lambda zip, as well as by the CDK template when creating lambda functions.
> 
> Lambda Config
> - `lambda.name`: This is used to generate the lambda zip file name, and is the name used when creating the lambda from CDK if using the CodersConduit CDK template with the included lambda stack.
> - `lambda.handler`: The lambda handler method, used by the CDK stack when creating the Lambda function.
>
> Build Config
> - `ccbuild.sources-root`: Package source directory. This typically should not change.
> - `ccbuild.test-root`: Package test directory. This typically should not change.
> - `ccbuild.dependencies-root`: Package dependencies' directory. Set this to the directory where your python dependencies are stored. It is recommended to utilize a venv stored in your packages root directory for your python lambda. By default, this is set to `venv/Lib/site-packages`.
