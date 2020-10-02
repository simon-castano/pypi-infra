# Welcome to Private Pypi Server Infrastructure

This repository contains the code for deploying a (private) [pypiserver](https://github.com/pypiserver/pypiserver) on AWS. Infrastructure is coded in [Python](https://www.python.org) with AWS [CDK](https://aws.amazon.com/cdk/) library.

## Installation

This project is set up like a standard Python project. It assumes that there are `python3` and `pipenv` executables in your path.

To manually create a virtualenv on MacOS and Linux:

```bash
pipenv install
```

At this point you can now synthesize the CloudFormation template for this code,

```bash
pipenv run cdk synth
```

or deploy the stack of your choice with

```bash
pipenv run cdk deploy <stack_name>
```

### Useful commands

Note: `pipenv run` must be prepended to the below commands.

*   `cdk ls`          list all stacks in the app
*   `cdk diff`        compare deployed stack with current state

#### Bootstrap

`cdk --profile integrations bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess`

## Usage

TODO

## Contributing

Please use `black` and `isort` for code formatting; `flake8`, `pydocstyle` and `mypy` for code linting.

## License

Copyright (c) 2020 Visualfabriq Revenue Management
