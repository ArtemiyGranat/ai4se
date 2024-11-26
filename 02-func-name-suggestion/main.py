import argparse
from pathlib import Path

from funccraft.data import download_dataset, load_dataset, prepare, save_dataset
from funccraft.models import predict


def main():
    args = parse_args()
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    default_data_path = Path('./prepared-dataset')
    prepare_data_parser = subparsers.add_parser('prepare-data')
    prepare_data_parser.set_defaults(func=prepare_data)
    # TODO: Use one flag for all options?
    prepare_data_parser.add_argument(
        '-p',
        '--dataset_path',
        help='Path to initial dataset',
        type=Path,
    )
    prepare_data_parser.add_argument(
        '-u',
        '--dataset_url',
        help='URL of initial dataset',
        type=str,
    )
    prepare_data_parser.add_argument(
        '-l',
        '--lang',
        help='Programming language which code is stored in initial dataset',
        type=str,
        choices=["python", "ruby"],
        default="python",
    )
    prepare_data_parser.add_argument(
        '-o',
        '--output',
        help='Path to save prepared dataset to',
        type=Path,
        default=default_data_path,
    )

    predict_parser = subparsers.add_parser('predict-names')
    predict_parser.set_defaults(func=predict_names)
    predict_parser.add_argument(
        '-d',
        '--dataset',
        help='Path to prepared dataset',
        type=Path,
        default=default_data_path,
    )
    predict_parser.add_argument(
        '-m',
        '--model',
        default='Salesforce/codet5p-220m',
    )

    return parser.parse_args()


def prepare_data(args):
    if not args.dataset_url and not args.dataset_path:
        raise RuntimeError("Neither the URL nor the path is specified")
    if args.dataset_url and args.dataset_path:
        raise RuntimeError("Either the path or the URL must be specified")

    dataset = (
        load_dataset(args.dataset_path)
        if args.dataset_path
        else download_dataset(args.dataset_url, args.lang)
    )
    dataset = prepare(dataset, args.lang)
    save_dataset(dataset, args.output)
    print(dataset[0])


def predict_names(args):
    dataset = load_dataset(args.dataset)
    predict(dataset, args.model)


if __name__ == '__main__':
    main()
