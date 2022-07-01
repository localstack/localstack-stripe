import atexit
import logging

from localstack.extensions.api import hooks, gateway, http, services

LOG = logging.getLogger(__name__)


@hooks.on_start()
def load_stripe_extension():
    LOG.info("loading stripe extension")

    from . import localstripe

    port = services.external_service_ports.reserve_port()
    localstripe.start(port)
    atexit.register(localstripe.shutdown)

    # create a proxy
    backend = f"http://localhost:{port}"
    endpoint = http.ProxyHandler(backend)

    # add proxy rules to gateway
    gateway.custom_routes.add(
        "/stripe",
        endpoint=endpoint,
    )
    gateway.custom_routes.add(
        "/stripe/<path:path>",
        endpoint=endpoint,
    )
    gateway.custom_routes.add(
        "/",
        host="stripe.localhost.localstack.cloud:<port>",
        endpoint=endpoint,
    )
    gateway.custom_routes.add(
        "/<path:path>",
        host="stripe.localhost.localstack.cloud:<port>",
        endpoint=endpoint,
    )
