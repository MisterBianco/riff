from riff import parser
from riff.contract import Contract

__version__ = "0.0.1"


def make_contract(filepath: str) -> Contract:
    return Contract(parser.parse(filepath))


def run(contract: Contract) -> None:
    contract.run()
