from loguru import logger

from riff.parser import parse_rule


class Contract:
    def __init__(self, rules: dict) -> None:
        self.url = rules["url"]

        self.rules = {
            k: parse_rule(v, self.url + k)
            for (k, v) in rules["endpoints"].items()
        }

        logger.info(f"Rules Parsed: {len(self.rules)}")
        logger.info(f"Contract Built\n")

    def __str__(self) -> str:
        return f"Riff_Contract(url={self.url}, {self.rules})"

    def run(self) -> None:
        for endpoint in self.rules.values():
            endpoint.run()
