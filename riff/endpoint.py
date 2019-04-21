import json

from typing import Union, Any
from http import HTTPStatus

import requests
from loguru import logger


class ContractViolationError(Exception):
    pass


class Endpoint:
    def __init__(
        self,
        url: str,
        method: str,
        code: Union[str, int],
        params: Any,
        headers: dict,
        jsonobj: Any,
        textobj: Any,
    ) -> None:
        self.url = url
        self.method = method or "get"
        self.params = params
        self.headers = headers

        self.code = code if type(code) is int else getattr(HTTPStatus, code)
        self.json = jsonobj if jsonobj else jsonobj
        logger.info(f"Endpoint Created: {self.url}")

    def __str__(self) -> str:
        return f"Endpoint(url={self.url})"

    def __repr__(self) -> str:
        return self.__str__()

    def run(self) -> None:
        logger.info(f"Running endpoint: {self.url}")

        request = getattr(requests, self.method)(
            self.url, headers=self.headers
        )

        if self.code:
            if request.status_code != self.code:
                raise ContractViolationError(
                    f"Request to {self.url} violates its contractional code {request.status_code} | {self.code}"
                )

        if self.json:
            resp_json = request.json()

            walker(resp_json, self.json)

            if request.json() != self.json:
                raise ContractViolationError(
                    f"Request to {self.url} violates its contractional response {request.json()} | {self.json}"
                )

        return


def walker(resp, match):
    # print("<", type(resp).__name__, type(match).__name__)
    if type(resp).__name__ == "dict":
        if match == "dict":
            return

        if resp.keys() != match.keys():
            # Method to find missing keys
            raise KeyError("Missing keys")

        for k, v in resp.items():
            if isinstance(v, dict) and isinstance(match[k], dict):
                walker(v, match[k])
            elif isinstance(v, list) and isinstance(match[k], list):
                walker(v, match[k])
            elif match[k] != v and type(v).__name__ != match[k]:
                raise ContractViolationError(f"{match[k]} != {v}")

    elif type(resp).__name__ == "list":
        if match == "list":
            return

        for i, v in enumerate(resp):
            if i >= len(match):
                raise ValueError(f"Contract index is missing: {i}")
            else:
                if isinstance(v, list) and (
                    isinstance(match[i], list) or match == "list"
                ):
                    print(resp[i], v)
                    walker(v, match[i])
                elif isinstance(v, dict) and (
                    isinstance(match[i], dict) or match == "dict"
                ):
                    print(v, match[i])
                    walker(v, match[i])
                elif match[i] != v and type(v).__name__ != match[i]:
                    # print(match[i], v, type(v).__name__)
                    raise ContractViolationError(f"{match[i]} != {v}")

    if type(resp) != type(match):
        raise ValueError("Type error")
