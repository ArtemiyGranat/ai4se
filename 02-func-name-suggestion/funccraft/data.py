from pathlib import Path

import datasets
import pandas as pd


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    print(df)
    return df


def load_dataset(path: Path) -> pd.DataFrame:
    return pd.DataFrame(datasets.load_from_disk(str(path)))


def download_dataset(url: str, lang: str) -> pd.DataFrame:
    return pd.DataFrame(
        datasets.load_dataset(url, lang, trust_remote_code=True, split="test")
    )


def save_dataset(dataset: pd.DataFrame, path: Path) -> None:
    dataset = datasets.Dataset.from_pandas(dataset)
    dataset.save_to_disk(str(path))
