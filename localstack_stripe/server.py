import multiprocessing
import sys

from localstack.utils.serving import Server
from localstripe.server import start as start_localstripe

from localstack_stripe.config import LOCALSTRIPE_PORT


class LocalstripeServer(Server):
    def __init__(self):
        super().__init__(LOCALSTRIPE_PORT)
        self.process = multiprocessing.Process(target=self._run_server)

    def do_shutdown(self):
        self.process.close()

    def do_run(self):
        self.process.start()
        self.process.join()

    @staticmethod
    def _run_server():
        sys.argv = [__file__, "--port", str(LOCALSTRIPE_PORT)]
        return start_localstripe()
