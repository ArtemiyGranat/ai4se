from pathlib import Path

import datasets
import pandas as pd
from tqdm import tqdm

from toxic_clf.process import (
    expand_contraction,
    remove_repetitions,
    remove_special_symbols,
    remove_url,
    resolve_profane_words,
    remove_programming_keywords,
)


def prepare(raw_data: Path) -> datasets.Dataset:
    dataset = (
        pd.read_excel(raw_data)
        .drop_duplicates()
        .dropna()
        .reset_index(drop=True)
        .assign(message=lambda x: x["message"].str.lower())
    )

    transformations = [
        remove_url,
        expand_contraction,
        remove_repetitions,
        remove_special_symbols,
        resolve_profane_words,
        remove_programming_keywords,
    ]
    for transform in tqdm(transformations):
        dataset["message"] = dataset.apply(transform, axis=1)

    return datasets.Dataset.from_pandas(dataset)


def load_dataset(path: Path) -> pd.DataFrame:
    return pd.DataFrame(datasets.load_from_disk(str(path)))


def save_dataset(dataset: pd.DataFrame, path: Path) -> None:
    dataset = datasets.Dataset.from_pandas(dataset)
    dataset.save_to_disk(str(path))
