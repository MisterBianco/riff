#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import riff
import click


@click.command()
@click.option(
    "-c", "--contract", default="contract.yml", help="Contract File Location"
)
def execute_contract(contract):
    """Contractual API Testing"""
    contract = riff.make_contract(contract)
    contract.run()


if __name__ == "__main__":
    execute_contract(prog_name="riff")
