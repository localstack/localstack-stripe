#!/usr/bin/env python
from setuptools import setup

entry_points = {
    "localstack.hooks.on_infra_start": [
        "load_stripe_extension=localstack_stripe.extension:load_stripe_extension"
    ],
}

setup(entry_points=entry_points)
