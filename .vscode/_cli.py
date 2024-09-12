import os
import runpy
import sys

TEST_PREFIX = os.environ.get(f"PSTEST_TEST_PREFIX")
TEST_SUFFIX = os.environ.get(f"PSTEST_TEST_SUFFIX")


def main() -> None:
    command = sys.argv[1]
    if command == "test":
        main_path = sys.argv[2]
        test_path = _infer_test_path(main_path)
        if os.path.exists(test_path):
            os.environ["PSTEST_MAIN"] = main_path
            run_unittest(test_path)
        else:
            run_unittest(main_path)


def run_unittest(filename: str) -> None:
    sys.path[0] = ""

    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m unittest"
    sys.argv = [sys.argv[0], filename]

    runpy.run_module("unittest", init_globals={}, run_name="__main__")


def _infer_test_path(main_path: str) -> str:
    main_dir = os.path.dirname(main_path)
    main_name, file_ext = os.path.splitext(os.path.basename(main_path))
    problem_name = main_name.split(".")[0]

    test_prefix = TEST_PREFIX or ""
    test_suffix = TEST_SUFFIX or ""
    test_filename = f"{test_prefix}{problem_name}{test_suffix}{file_ext}"
    return os.path.join(main_dir, test_filename)


if __name__ == "__main__":
    main()
