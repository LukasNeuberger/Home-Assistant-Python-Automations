import asyncio


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = None
        self.state = "CREATED"

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()
        self.state = "FINISHED"

    def start(self):
        self._task = asyncio.ensure_future(self._job())
        self.state = "RUNNING"

    def cancel(self):
        self._task.cancel()
        self._task = None
        self.state = "CANCELED"
