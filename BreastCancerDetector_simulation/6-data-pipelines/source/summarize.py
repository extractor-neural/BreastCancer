import argparse
import os

import pandas as pd
import yaml


def main():
    args = parse_args()
    config = load_config(args.yaml_file)

    letter_data = concat_source_files(config["letter_source"])
    letter_data = letter_data[["date", "day_name", "letter"]]
    letter_data = letter_data.set_index("date")

    web_data = concat_source_files(config["web_source"])
    web_data = web_data[["date", "web"]]
    web_data = web_data.set_index("date")

    data = pd.concat([letter_data, web_data], axis="columns")
    data = data.reset_index()

    save_data(data, config["destination"])


def save_data(data, destination_dir):
    data.to_csv(os.path.join(destination_dir, "data.csv"), index=False)


def concat_source_files(source_dir):
    files = os.listdir(source_dir)
    data = pd.DataFrame()
    for file in files:
        file_path = os.path.join(source_dir, file)
        data = pd.concat([data, pd.read_csv(file_path)])
    data = data.sort_values("date")
    return data


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
