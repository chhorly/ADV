from abc import ABC, abstractmethod

import pandas as pd


class DataTransform(ABC):
    @abstractmethod
    def apply(self, df):
        pass


class DropMissingTransform(DataTransform):
    def apply(self, df):
        return df.dropna()


class MeanFillTransform(DataTransform):
    def apply(self, df):
        return df.fillna(df.mean(numeric_only=True))


class MinMaxScaleTransform(DataTransform):
    def apply(self, df):
        transformed = df.copy()
        numeric_columns = transformed.select_dtypes(include="number").columns
        for column in numeric_columns:
            minimum = transformed[column].min()
            value_range = transformed[column].max() - minimum
            if value_range == 0:
                transformed[column] = 0
            else:
                transformed[column] = (transformed[column] - minimum) / value_range
        return transformed


class TransformFactory:
    _transforms = {
        "drop_missing": DropMissingTransform,
        "fill_mean": MeanFillTransform,
        "min_max_scale": MinMaxScaleTransform,
    }

    @classmethod
    def create(cls, transform_name):
        try:
            transform_class = cls._transforms[transform_name]
        except KeyError as error:
            available = ", ".join(sorted(cls._transforms))
            raise ValueError(
                f"Unknown transform {transform_name!r}. "
                f"Choose one of: {available}"
            ) from error
        return transform_class()


if __name__ == "__main__":
    data = pd.DataFrame(
        {
            "score": [10.0, None, 30.0],
            "visits": [2, 4, 6],
            "category": ["A", "B", "A"],
        }
    )

    transform = TransformFactory.create("fill_mean")
    print(transform.apply(data))
