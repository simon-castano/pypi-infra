#!/usr/bin/env python3
from aws_cdk.core import App

from pypi_infra import PypiserverInfra


def main() -> None:
    app = App()
    PypiserverInfra(app, "pypiserver-infrastructure")
    app.synth()


if __name__ == "__main__":
    main()
