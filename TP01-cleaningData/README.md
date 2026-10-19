# TP-1: Cleaning Data with OOP and Design Patterns

This project presents the exercises in separate files. Each file focuses on
the concepts introduced in that exercise; Exercise 5 imports and combines the
previous components into a complete pipeline.

## Requirements

- Python 3
- pandas

Install pandas if needed:

```bash
python -m pip install pandas
```

## Exercise 1: CSV reader

[`ex1.py`](./ex1.py) defines `CSVReader`, which stores a file path, loads CSV
data with `read()`, and prints the first `n` rows with `preview(n)`.

```python
from ex1 import CSVReader

reader = CSVReader(
    "sample_data (2).csv"
)
data = reader.read()
reader.preview(5)
```

Running `python ex1.py` from this directory also reads the included CSV and
prints its first five rows.

## Exercise 2: Missing-value Strategy Pattern

[`ex2.py`](./ex2.py) defines the abstract `MissingValueStrategy` interface and
three interchangeable implementations:

- `DropMissingValuesStrategy`: drops rows containing missing values.
- `MeanFillStrategy`: fills missing numeric values with their column means.
- `ModeFillStrategy`: fills missing values using the first mode in each column.

`DataCleaner` accepts a strategy and applies it with `clean(df)`.

```python
from ex1 import CSVReader
from ex2 import DataCleaner, MeanFillStrategy

data = CSVReader("input.csv").read()
cleaned_data = DataCleaner(MeanFillStrategy()).clean(data)
```

## Exercise 3: Logging and timing decorators

[`ex3.py`](./ex3.py) defines the reusable `log_call` and `timeit` decorators
and applies both to `CSVReader.read()`. It contains the decorated version of
the reader from Exercise 1.

To see the informational log messages, configure logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

## Exercise 4: Transformation Factory

[`ex4.py`](./ex4.py) defines the abstract `DataTransform.apply(df)` interface
and the `TransformFactory`. The prompt does not specify which transformation
subclasses to implement, so this project provides these examples relevant to
cleaning data:

- `"drop_missing"`: drop rows containing missing values.
- `"fill_mean"`: fill missing numeric values with their column means.
- `"min_max_scale"`: scale numeric columns to the range 0–1; constant columns
  become 0.

```python
from ex4 import TransformFactory

transform = TransformFactory.create("min_max_scale")
transformed_data = transform.apply(cleaned_data)
```

An unknown factory name raises `ValueError` and lists the supported names.

## Exercise 5: Template Method cleaning pipeline

[`ex5.py`](./ex5.py) defines the abstract `DataPipeline` workflow in `run()`:
load the CSV, clean missing values, then apply a transformation. Its
`CSVDataPipeline` uses the reader from Exercise 3, the strategy cleaner from
Exercise 2, and the transformation factory from Exercise 4. Running
`python ex5.py` prints the data after missing-value cleaning, before the
transformation is applied.

```python
from ex2 import MeanFillStrategy
from ex5 import CSVDataPipeline

pipeline = CSVDataPipeline(
    file_path="sample_data (2).csv",
    strategy=MeanFillStrategy(),
    transform_name="min_max_scale",
)
cleaned_data = pipeline.run()
print(cleaned_data.head())
```

Run scripts from this directory so imports such as `from ex2 import ...`
resolve correctly.
