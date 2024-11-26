from pathlib import Path

import datasets
import pandas as pd
from tree_sitter import Language, Parser

from funccraft.process import extract_func_info
from funccraft.languages import AVAILABLE_LANGUAGES, FIELDS, QUERIES


def prepare(dataset: datasets.Dataset, lang: str) -> pd.DataFrame:
    lang_obj = Language(AVAILABLE_LANGUAGES[lang])
    parser = Parser(lang_obj)
    query = lang_obj.query(QUERIES[lang])

    return dataset.map(
        lambda row: extract_func_info(FIELDS[lang], parser, query, row)
    )


def load_dataset(path: Path) -> pd.DataFrame:
    return datasets.load_from_disk(str(path))


def download_dataset(url: str, lang: str) -> pd.DataFrame:
    return datasets.load_dataset(
        url, lang, trust_remote_code=True, split="test"
    )


def save_dataset(dataset: datasets.Dataset, path: Path) -> None:
    dataset.save_to_disk(str(path))
