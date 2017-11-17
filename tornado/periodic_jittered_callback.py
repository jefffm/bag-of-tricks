import random

from tornado.ioloop import PeriodicCallback, IOLoop


class PeriodicJitteredCallback(PeriodicCallback):
    def __init__(self, callback, callback_time, jitter_pct=10, io_loop=None):

        self.callback = callback
        if callback_time <= 0:
            raise ValueError(
                "Periodic callback must have a positive callback_time")

        self.io_loop = io_loop or IOLoop.current()
        self._running = False
        self._timeout = None

        self._configured_callback_time = callback_time
        self.jitter_pct = jitter_pct

    @staticmethod
    def _calculate_jitter(interval, jitter_pct):
        assert 0 <= jitter_pct <= 100

        # Convert jitter_pct  to a decimal percentage
        jitter = 0.1 * random.randint(0, jitter_pct)

        # Return the interval plus some jitter
        return interval + (interval * jitter)
