from pathlib import Path

import datasets
import pandas as pd

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

available_langs = {
    "python": tspython.language(),
}


def prepare(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    parser = Parser(Language(available_langs[lang]))
    # print(df.iloc[0]["whole_func_string"])
    tree = parser.parse(bytes(df.iloc[0]["whole_func_string"], "utf8"))

    root_node = tree.root_node
    print(root_node.children)
    function_node = root_node.children[0]
    print(function_node.child_by_field_name("name").text)
    print(function_node.child_by_field_name("body").text)

    # print(df)
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
