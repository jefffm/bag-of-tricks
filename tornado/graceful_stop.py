import logging

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback

SHUTDOWN_TIMEOUT = 5

LOG = logging.getLogger(__name__)


def _final_stop(ioloop):
    # type: (IOLoop) => None
    ioloop.stop()


def graceful_shutdown(ioloop, httpserver):
    # type: (IOLoop, HTTPServer) -> None
    def _wait():
        # Ignore the internal tornado "waker" handler
        remaining_handlers = {
            k: v
            for k, v in ioloop._handlers.items()
            if k != ioloop._waker.fileno()
        }

        # It's safe to shutdown when no handlers remain
        remaining_count = len(remaining_handlers)
        if remaining_count == 0:
            _final_stop(ioloop)
        else:
            LOG.info('Waiting on IO handlers (%s remaining). '
                     'Handlers: %s', remaining_count, remaining_handlers)

    # Stop accepting new http requests
    httpserver.stop()

    # Wait for all handlers to complete
    poller = PeriodicCallback(_wait, 500, io_loop=ioloop)
    poller.start()

    ioloop.add_timeout(ioloop.time() + SHUTDOWN_TIMEOUT, _final_stop)
