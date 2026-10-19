from pathlib import Path

import pandas as pd


class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read(self):
        self.data = pd.read_csv(self.file_path)
        return self.data

    def preview(self, n=5):
        if self.data is None:
            self.read()
        print(self.data.head(n))


if __name__ == "__main__":
    csv_path = Path(__file__).with_name("sample_data (2).csv")
    reader = CSVReader(csv_path)
    reader.read()
    reader.preview(5)
