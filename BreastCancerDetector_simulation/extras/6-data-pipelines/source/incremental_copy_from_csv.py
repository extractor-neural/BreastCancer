import argparse
import os
from datetime import datetime

import pandas as pd
import yaml


def main():
    args = parse_args()
    config = load_config(args.yaml_file)
    data = get_incremental_data(config)
    save_data(config, data)


def save_data(config, data):
    out_file = config["destination"].format(
        datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
    )
    data.to_csv(out_file, index=False)


def get_incremental_data(config):
    last_modified = get_last_modified(config)
    data = pd.read_csv(config["source"])
    data = data[data.last_modified > last_modified]
    return data


def get_last_modified(config):
    filename = get_last_file(config)
    destination_dir = os.path.dirname(config["destination"])
    filename = os.path.join(destination_dir, filename)
    data = pd.read_csv(filename)
    last_modified = data.last_modified.tail(1).values[0]
    return last_modified


def get_last_file(config):
    destination_dir = os.path.dirname(config["destination"])
    files = os.listdir(destination_dir)
    files.sort()
    return files[-1]


def load_config(yaml_file):
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../config", yaml_file)
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {yaml_file} not found")
    with open(filename, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
