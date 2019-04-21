from riff import parser
from riff.contract import Contract

__version__ = "0.0.2-Beta"


def make_contract(filepath: str) -> Contract:
    return Contract(parser.parse_yaml(filepath))
