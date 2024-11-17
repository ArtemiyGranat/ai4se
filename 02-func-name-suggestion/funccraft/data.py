from pathlib import Path

import datasets
import pandas as pd

from tree_sitter import Language, Parser

from funccraft.languages import AVAILABLE_LANGUAGES, QUERIES


def prepare(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    lang_obj = Language(AVAILABLE_LANGUAGES[lang])
    parser = Parser(lang_obj)
    query = lang_obj.query(QUERIES[lang])

    for index, row in df.iterrows():
        tree = parser.parse(bytes(row["whole_func_string"], "utf8"))
        captures = query.captures(tree.root_node)

        df.at[index, "func_name"] = captures["name"][0].text.decode("utf8")
        df.at[index, "func_body"] = captures["body"][0].text.decode("utf8")
        # There are functions without body in a dataset
        if "body-without-comments" in captures:
            df.at[index, "func_body_without_comments"] = '\n'.join(
                [
                    line.text.decode("utf8")
                    for line in captures["body-without-comments"]
                ]
            )

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
