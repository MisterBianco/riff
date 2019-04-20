#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append("/home/jacobsin/Development/python/rifflib")

import riff

# contract = riff.make_contract("contract.yml")
riff.endpoint.walker(
    [{
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": {
            "grrr": [
                "test"
            ]
        }
    }], 
    ["dict", "dict", "dict", "dict", {
        "userId": "int",
        "id": "int",
        "title": "str",
        "body": {"str": "list"}
    }]
)