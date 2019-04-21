#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import riff
import click


@click.command()
@click.option(
    "-c", "--contract", default="contract.yml", help="Contract File Location"
)
@click.option(
    "-e", "--endpoint", default="", help="Endpoint to run, exclude for all"
)
def execute_contract(contract: str, endpoint: str) -> int:
    """Contractual API Testing"""

    contract = riff.make_contract(contract)

    if not endpoint:
        contract.run()
    else:
        contract.endpoints[endpoint].run()

    return 0


if __name__ == "__main__":
    execute_contract(prog_name="riff")
