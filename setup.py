#!/usr/bin/env python
from setuptools import setup

entry_points = {
    "localstack.aws.provider": ["stripe:default=localstack_stripe.plugin:LocalstripeServicePlugin"],
    "localstack.hooks.prepare_host": [
        "announce_localstripe=localstack_stripe.plugin:announce_localstripe"
    ],
    "localstack.hooks.configure_localstack_container": [
        "expose_stripe_port=localstack_stripe.plugin:expose_stripe_port"
    ],
    "localstack.hooks.on_infra_start": [
        "register_localstripe_route=localstack_stripe.plugin:register_localstripe_route"
    ],
}


setup(entry_points=entry_points)
