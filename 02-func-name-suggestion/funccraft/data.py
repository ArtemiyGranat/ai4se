from pathlib import Path

import datasets
import pandas as pd
from tree_sitter import Language, Parser

from funccraft.languages import AVAILABLE_LANGUAGES, FIELDS, QUERIES


def prepare(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    lang_obj = Language(AVAILABLE_LANGUAGES[lang])
    parser = Parser(lang_obj)
    query = lang_obj.query(QUERIES[lang])

    for idx, row in df.iterrows():
        func_string = row["whole_func_string"]
        tree = parser.parse(bytes(func_string, "utf8"))
        captures = query.captures(tree.root_node)
        print(captures)

        comments = []
        for capture in captures:
            nodes = captures[capture]
            for node in nodes:
                if capture in FIELDS[lang]["name"]:
                    df.at[idx, "func_name"] = func_string[
                        node.start_byte : node.end_byte
                    ]
                elif capture in FIELDS[lang]["body"]:
                    df.at[idx, "func_body"] = func_string[
                        node.start_byte : node.end_byte
                    ]
                elif capture in FIELDS[lang]["comment"]:
                    comments.append(
                        func_string[node.start_byte : node.end_byte]
                    )

        body_without_comment = df.at[idx, "func_body"]
        for comment in comments:
            body_without_comment = body_without_comment.replace(comment, "")
        df.at[idx, "body_without_comments"] = body_without_comment

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
