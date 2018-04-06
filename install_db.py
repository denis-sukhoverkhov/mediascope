import argparse
import logging
import zipfile

import os

import sys


def create_parser():
    arg_parser = argparse.ArgumentParser(description='Unpack db-files')
    arg_parser.add_argument('--path', type=str, default='./tmp/dbs.zip', help='path to zip archive of db')
    return arg_parser


def main(arguments):
    if not os.path.exists(arguments.path):
        error_message = f'File does not exist: {args.path}'
        logging.exception(error_message)
        sys.exit(error_message)

    with zipfile.ZipFile(arguments.path, "r") as zip_ref:
        zip_ref.extractall('./')


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
