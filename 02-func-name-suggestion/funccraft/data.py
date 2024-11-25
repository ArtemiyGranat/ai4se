from pathlib import Path

import datasets
import pandas as pd

from tree_sitter import Language, Parser

from funccraft.languages import AVAILABLE_LANGUAGES, QUERIES


def prepare(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    lang_obj = Language(AVAILABLE_LANGUAGES[lang])
    parser = Parser(lang_obj)
    query = lang_obj.query(QUERIES[lang])

    for idx, row in df.iterrows():
        func_string = row["whole_func_string"]
        tree = parser.parse(bytes(func_string, "utf8"))
        captures = query.captures(tree.root_node)

        df.at[idx, "func_name"] = captures["name"][0].text.decode("utf8")
        df.at[idx, "func_body"] = captures["body"][0].text.decode("utf8")
        print(captures)
        comments = [
            func_string[node.start_byte : node.value.end_byte]
            for node, capture_name in captures
            if capture_name in ["comment", "docstring"]
        ]

        body_without_comment = df.at[idx, "func_name"]
        for comment in comments:
            body_without_comment = body_without_comment.replace(comment, "")
        df.at[idx, "body_without_comments"] = body_without_comment
        print(body_without_comment)
        return

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
