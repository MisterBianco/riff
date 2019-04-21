import re
import yaml
import os.path

from loguru import logger

from riff.endpoint import Endpoint


class ContractViolationError(Exception):
    pass


ENDPOINT_KEYS = ["method", "code", "json", "text", "headers", "params"]

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
    logger.info(f"Validating url: {url}")
    if not re.match(URL_REGEX, url):
        raise InvalidURLException(f"{url} is not a valid url")
    return True


def parse_yaml(filepath: str) -> dict:
    if os.path.isfile(filepath):
        with open(filepath, "r") as filehandle:
            return yaml.load(filehandle, Loader=yaml.FullLoader)
    raise FileNotFoundError(f"File: {filepath} is not a file")


def parse_rule(rule: dict, url: str) -> None:
    validate_url(url)

    logger.info(f"Parsing Rule: {url}")

    [bad_key(key) for key in rule.keys() if key not in ENDPOINT_KEYS]

    return Endpoint(
        url=url,
        method=rule.get("method", None),
        code=rule.get("code", None),
        params=rule.get("params", None),
        headers=rule.get("headers", None),
        jsonobj=rule.get("json", None),
        textobj=rule.get("text", None),
    )


def bad_key(key: str):
    raise KeyError(f"Bad key in endpoint rule: {key}")


def type_cmp(resp, match):
    return type(resp) == type(match) or type(resp).__name__ == match


def is_dict(obj):
    return type(obj).__name__ == "dict"


def is_list(obj):
    return type(obj).__name__ == "list"


def parse_response(resp, match):

    if is_dict(resp):
        if match == "dict":
            return

        if resp.keys() != match.keys():
            # Method to find missing keys
            raise KeyError("Missing keys")

        for k, v in resp.items():
            if is_dict(v) and is_dict(match[k]):
                walker(v, match[k])
            elif is_list(v) and is_list(match[k]):
                walker(v, match[k])
            elif not type_cmp(v, match[k]):
                raise ContractViolationError(f"{v} != {match[k]}")

    elif is_list(resp):
        if match == "list":
            return

        for i, v in enumerate(resp):
            if i >= len(match):
                raise ValueError(f"Contract index is missing: {i}")
            else:
                if is_list(v) and (is_list(match[i]) or match == "list"):
                    walker(v, match[i])
                elif is_dict(v) and (is_dict(match[i]) or match == "dict"):
                    walker(v, match[i])
                elif not type_cmp(v, match[i]):
                    raise ContractViolationError(f"{match[i]} != {v}")

    if not type_cmp(resp, match):
        raise ValueError("Type error")
