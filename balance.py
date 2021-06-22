import json
import math
import os
from zipfile import ZipFile

import click

from generate import generate_images


def balance_ds(label_to_name: dict, label_counts: dict, abs_network_path: str, abs_out_dir: str,
               amplifier: float = 1.0):
    max_generate = math.ceil(max(label_counts.values()) * amplifier)
    for label in label_counts:
        how_many = max_generate - label_counts[label]
        where = abs_out_dir + os.path.sep + label_to_name[label]
        if how_many > 0:
            generate_images(network_pkl=abs_network_path, seeds=list(range(how_many)), outdir=where, class_idx=label)


@click.command()
@click.option('--zip_path', 'for_sg2ada_zip_path', type=str, required=True)
@click.option('--network', 'abs_network_path', type=str, required=True)
@click.option('--out_dir', 'abs_out_dir', type=str, required=True, metavar='DIR')
@click.option('--amplifier', type=float, default=1, show_default=True)
def balance(for_sg2ada_zip_path: str, abs_network_path: str, abs_out_dir: str, amplifier: float = 1.0):
    with ZipFile(for_sg2ada_zip_path, 'r') as zip:
        with zip.open('dataset.json', 'r') as dataset_json:
            label_to_name = json.load(dataset_json)['label_to_name']
            label_counts = json.load(dataset_json)['label_counts']
    balance_ds(label_to_name, label_counts, abs_network_path, abs_out_dir, amplifier)


if __name__ == '__main__':
    balance()
