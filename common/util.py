import datetime
import io
import resource
import runpy
import signal
import textwrap
import unittest
from contextlib import contextmanager, redirect_stdout, _RedirectStream, nullcontext


class Time(datetime.timedelta):
    pass


class MemorySize:
    def __init__(self, mb: float = None) -> None:
        self._size = int(mb * 1024 * 1024)

    @property
    def size(self) -> int:
        return self._size


class PSTestCase(unittest.TestCase):
    problem_url: str | None
    time_limit: Time | None
    memory_limit: MemorySize | None

    def assertTC(self, module: str, input: str, output: str) -> None:
        input = self.refine(input)
        output = self.refine(output)

        input_stream = io.StringIO(input)
        output_stream = io.StringIO()
        with (redirect_stdin(input_stream),
              redirect_stdout(output_stream),
              timeout(self.time_limit.total_seconds()) if self.time_limit else nullcontext(),
              memory_limit(self.memory_limit.size) if self.memory_limit else nullcontext()):
            runpy.run_path(module, run_name='__main__')
        result = self.refine(output_stream.getvalue())

        self.assertEqual(result, output)

    def refine(self, s: str) -> str:
        return textwrap.dedent(s).strip()


class redirect_stdin(_RedirectStream):
    """Context manager for temporarily receiving stdin from another source."""
    _stream = 'stdin'


@contextmanager
def timeout(seconds: float):
    def _handler(signum, frame):
        raise TimeoutError('Time Limit Exceeded')
    signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)

    try:
        yield
    except TimeoutError:
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


@contextmanager
def memory_limit(size: int):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (size, hard))

    try:
        yield
    finally:
        resource.setrlimit(resource.RLIMIT_AS, (soft, hard))
