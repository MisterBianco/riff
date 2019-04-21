import os
import riff


def test_version():
    assert riff.__version__ == "0.0.1"


def test_walker():
    riff.endpoint.walker(
        [
            {
                "userId": 1,
                "id": 1,
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": {"grrr": ["test"]},
            }
        ],
        [
            "dict",
            "dict",
            "dict",
            "dict",
            {
                "userId": "int",
                "id": "int",
                "title": "str",
                "body": {"str": "list"},
            },
        ],
    )


def test_walker_deep():
    riff.endpoint.walker(
        [{"1": [{"1": [{"1": ["1"]}]}]}], [{"1": [{"1": [{"1": ["str"]}]}]}]
    )


def test_walker_wildcards():
    riff.endpoint.walker(
        {
            "integer": 1,
            "string": "hello",
            "array": [1, 2, 3],
            "map": {"TEST": "WORLD"},
        },
        {"integer": "int", "string": "str", "array": "list", "map": "dict"},
    )
