from functools import wraps
import logging
from pathlib import Path
from time import perf_counter

import pandas as pd


logger = logging.getLogger(__name__)


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Calling %s", func.__qualname__)
        return func(*args, **kwargs)

    return wrapper


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = perf_counter() - start_time
            logger.info("%s completed in %.6f seconds", func.__qualname__, elapsed_time)

    return wrapper


class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    @log_call
    @timeit
    def read(self):
        self.data = pd.read_csv(self.file_path)
        return self.data

    def preview(self, n):
        if self.data is None:
            self.read()
        print(self.data.head(n))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    csv_path = Path(__file__).with_name("sample_data (2).csv")
    reader = CSVReader(csv_path)
    reader.read()
    reader.preview(5)
