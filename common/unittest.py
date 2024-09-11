import datetime
import io
import os
import re
import runpy
import textwrap
import unittest
from contextlib import redirect_stdout, nullcontext
from .util import redirect_stdin, timeout, memory_limit

USER_SUFFIX = os.environ.get('USER_SUFFIX' ,'')


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

        output_stream = io.StringIO()
        with (redirect_stdin(io.StringIO(input)),
              redirect_stdout(output_stream),
              timeout(self.time_limit.total_seconds()) if self.time_limit else nullcontext(),
              memory_limit(self.memory_limit.size) if self.memory_limit else nullcontext()):
            runpy.run_path(module, run_name='__main__')
        result = self.refine(output_stream.getvalue())

        self.assertEqual(result, output)

    def refine(self, s: str) -> str:
        return textwrap.dedent(s).strip()


def parse_testpath(filepath: str) -> tuple[str, str]:
    base_dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    problem_name = re.match(r'^(.*)_test\.py$', filename).group(1)
    return base_dir, problem_name
