import json

from http import HTTPStatus

import requests
from loguru import logger

from riff import parser


class Endpoint:
    def __init__(
        self, url, method, code, params, headers, jsonobj, textobj
    ) -> None:

        if not jsonobj and not textobj:
            raise ValueError(
                "Endpoint must have a text or json result contract."
            )

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
            parser.parse_response(request.json(), self.json)
        return
