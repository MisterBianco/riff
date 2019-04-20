import re

from typing import List, Dict

from riff.endpoint import Endpoint


URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def validate_url(url: str) -> bool:
    if not re.match(URL_REGEX, url):
        raise InvalidURLException(f"{url} is not a valid url")
    return True


class Contract:
    def __init__(self, laws: dict) -> None:
        self.url = None
        self.endpoints = []

        self.parse(laws)

    def __str__(self) -> str:
        return f"Riff_Contract(url={self.url}, {self.endpoints})"

    def parse(self, laws: dict) -> None:
        self.url = laws["url"]
        validate_url(self.url)

        for key in laws["endpoints"].keys():
            self.endpoints.append(
                Endpoint(
                    url=self.url + key,
                    method=laws["endpoints"][key].get("method", None),
                    code=laws["endpoints"][key].get("code", None),
                    params=laws["endpoints"][key].get("params", None),
                    headers=laws["endpoints"][key].get("headers", None),
                    jsonobj=laws["endpoints"][key].get("json", None),
                    textobj=laws["endpoints"][key].get("text", None),
                )
            )

    def run(self) -> None:
        for endpoint in self.endpoints:
            endpoint.run()
