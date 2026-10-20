"""Workers only enqueue callbacks. drain() runs them on the caller's thread."""

from concurrent.futures import ThreadPoolExecutor
from itertools import count
from queue import Empty, Queue


class TaskRunner:
    def __init__(self, workers=4):
        self._executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="launcher")
        self._callbacks = Queue()
        self._handlers = {}
        self._tokens = count()
        self._closed = False

    def post(self, callback):
        if not self._closed:
            self._callbacks.put(callback)

    def submit(self, work, on_success, on_error):
        if self._closed:
            return
        token = next(self._tokens)
        # Keep presentation handlers on the caller's thread. Workers only retain
        # a token and plain results, so closing cannot finalize Tk objects there.
        self._handlers[token] = (on_success, on_error)

        def execute():
            try:
                value = work()
            except Exception as error:
                self.post(lambda error=error: self._deliver(token, False, error))
            else:
                self.post(lambda: self._deliver(token, True, value))

        self._executor.submit(execute)

    def _deliver(self, token, succeeded, value):
        handlers = self._handlers.pop(token, None)
        if handlers is not None:
            handlers[0 if succeeded else 1](value)

    def drain(self):
        for _ in range(100):
            try:
                callback = self._callbacks.get_nowait()
            except Empty:
                break
            if not self._closed:
                callback()

    def close(self):
        self._closed = True
        self._handlers.clear()
        while True:
            try:
                self._callbacks.get_nowait()
            except Empty:
                break
        self._executor.shutdown(wait=False, cancel_futures=True)
