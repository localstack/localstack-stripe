import threading

from localstack.runtime import hooks
from localstack.services.generic_proxy import EndpointProxy
from localstack.services.plugins import PLUGIN_NAMESPACE, SERVICE_PLUGINS, Service, ServicePlugin
from localstack.utils.bootstrap import LocalstackContainer

from localstack_stripe.config import LOCALSTRIPE_PORT


@hooks.configure_localstack_container()
def expose_stripe_port(container: LocalstackContainer):
    container.ports.add(LOCALSTRIPE_PORT)


@hooks.prepare_host()
def announce_localstripe():
    print("this localstack instance will have stripe")


@hooks.on_infra_start()
def register_localstripe_route():
    LazyEndpointProxy(
        "/stripe", f"http://localhost:{LOCALSTRIPE_PORT}", load_stripe_service
    ).register()


def load_stripe_service():
    SERVICE_PLUGINS.require("stripe")


class LocalstripeServicePlugin(ServicePlugin):
    namespace = PLUGIN_NAMESPACE
    name = "stripe:default"
    api = "stripe"

    def create_service(self) -> Service:
        from localstack_stripe.server import LocalstripeServer

        server = LocalstripeServer()

        def _start(*args, **kwargs):
            server.start()
            server.wait_is_up()

        def _check(expect_shutdown=False, print_error=False):
            if expect_shutdown:
                assert not server.is_up()
            else:
                assert server.is_up()

        service = Service(self.api, start=_start, check=_check)
        service.default_active = True
        return service


class LazyEndpointProxy(EndpointProxy):
    def __init__(self, base_url: str, forward_url: str, init_method) -> None:
        super().__init__(base_url, forward_url)
        self.init_method = init_method

        self.is_init_called = False
        self.mutex = threading.RLock()

    def forward_request(self, method, path, data, headers):
        host = headers.get("Host", "")

        if self.forwarder.matches(host, path):
            if not self.is_init_called:
                if self.mutex:
                    if not self.is_init_called:
                        self.init_method()

        return self.forwarder.forward_request(method, path, data, headers)
