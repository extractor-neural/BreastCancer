import argparse
import os

import pandas as pd
import yaml


def main():
    args = parse_args()
    config = load_config(args.yaml_file)
    in_files = os.listdir(config["source"])
    out_files = os.listdir(config["destination"])
    new_files = get_new_files(in_files, out_files)
    process_files(config, new_files)


def process_files(config, files):
    for file in files:
        in_file = os.path.join(config["source"], file)
        out_file = os.path.join(config["destination"], file)
        data = pd.read_csv(in_file)
        data = data.dropna()
        data = data.drop_duplicates()
        data.to_csv(out_file, index=False)


def get_new_files(in_files, out_files):
    new_files = set(in_files) - set(out_files)
    return new_files


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", type=str)
    args = parser.parse_args()
    return args


def load_config(yaml_file):
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../config", yaml_file)
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {yaml_file} not found")
    with open(filename, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


if __name__ == "__main__":
    main()
