import argparse
from pathlib import Path

from toxic_clf.data import load_dataset, prepare, save_dataset
from toxic_clf.models import classifier, predict


def main():
    args = parse_args()
    args.func(args)


# Add help messages everywhere
def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    default_data_path = Path("./prepared-dataset")
    prepare_data_parser = subparsers.add_parser("prepare-data")
    prepare_data_parser.set_defaults(func=prepare_data)
    prepare_data_parser.add_argument(
        "-i",
        "--input",
        help="path to load raw dataset",
        type=Path,
    )
    prepare_data_parser.add_argument(
        "-o",
        "--output",
        help="path to save prepared dataset to",
        type=Path,
        default=default_data_path,
    )

    train_model_parser = subparsers.add_parser("train")
    train_model_parser.set_defaults(func=classify)
    train_model_parser.add_argument(
        "-d",
        "--dataset",
        help="path to prepared dataset",
        type=Path,
        default=default_data_path,
    )
    train_model_parser.add_argument(
        "-m",
        "--model",
        choices=[
            "logistic_regression",
            "random_forest",
            "roberta-base",
            "microsoft/codebert-base",
        ],
        default="logistic_regression",
    )
    train_model_parser.add_argument(
        "-v",
        "--vectorizer",
        choices=[
            "count",
            "tfidf",
        ],
        default="tfidf",
    )
    train_model_parser.add_argument(
        "--checkpoint",
    )
    train_model_parser.add_argument("-t", "--test-size", type=float, default=0.2)

    classify_parser = subparsers.add_parser("classify")
    classify_parser.set_defaults(func=predict)
    classify_parser.add_argument(
        "-m", "--model", help="path to trained model's directory", required=True
    )
    classify_parser.add_argument(
        "-c", "--comment", help="code review comment", required=True
    )

    return parser.parse_args()


def prepare_data(args):
    dataset = prepare(args.input)
    save_dataset(dataset, args.output)


def classify(args):
    dataset = load_dataset(args.dataset)
    classifier(dataset, args.model, args.vectorizer, args.test_size, args.checkpoint)


if __name__ == "__main__":
    main()
