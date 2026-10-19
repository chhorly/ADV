from abc import ABC, abstractmethod
from pathlib import Path

from ex2 import DataCleaner, MeanFillStrategy
from ex3 import CSVReader
from ex4 import TransformFactory


class DataPipeline(ABC):
    def run(self):
        data = self.load_data()
        data = self.clean_data(data)
        return self.transform_data(data)

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def clean_data(self, data):
        pass

    @abstractmethod
    def transform_data(self, data):
        pass


class CSVDataPipeline(DataPipeline):
    def __init__(self, file_path, strategy, transform_name):
        self.reader = CSVReader(file_path)
        self.cleaner = DataCleaner(strategy)
        self.transform = TransformFactory.create(transform_name)

    def load_data(self):
        return self.reader.read()

    def clean_data(self, data):
        return self.cleaner.clean(data)

    def transform_data(self, data):
        return self.transform.apply(data)


if __name__ == "__main__":
    pipeline = CSVDataPipeline(
        file_path=Path(__file__).with_name("sample_data (2).csv"),
        strategy=MeanFillStrategy(),
        transform_name="min_max_scale",
    )
    raw_data = pipeline.load_data()
    cleaned_data = pipeline.clean_data(raw_data)
    print("Data after missing-value cleaning:")
    print(cleaned_data.to_string(index=False))
