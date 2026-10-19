from abc import ABC, abstractmethod


class MissingValueStrategy(ABC):
    @abstractmethod
    def handle(self, df):
        pass


class DropMissingValuesStrategy(MissingValueStrategy):
    def handle(self, df):
        return df.dropna()


class MeanFillStrategy(MissingValueStrategy):
    def handle(self, df):
        return df.fillna(df.mean(numeric_only=True))


class ModeFillStrategy(MissingValueStrategy):
    def handle(self, df):
        modes = df.mode()
        if modes.empty:
            return df.copy()
        return df.fillna(modes.iloc[0])


class DataCleaner:
    def __init__(self, strategy):
        self.strategy = strategy

    def clean(self, df):
        return self.strategy.handle(df)
