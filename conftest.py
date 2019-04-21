#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

import riff


# def pytest_addoption(parser):
#     parser.addoption(
#         "--headless",
#         action="store_true",
#         default=False,
#         help="Run headless browser",
#     )


@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless")


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)
