import argparse
import os
import shutil
from datetime import datetime

import yaml


def main():
    args = parse_args()
    config = load_config(args.yaml_file)
    copy_file(config)


def copy_file(config):
    in_file = config["source"]
    out_file = config["destination"].format(
        datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
    )
    shutil.copy(in_file, out_file)


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
