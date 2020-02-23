from tqdm import tqdm

import config as cfg
import pandas as pd


def split_data_to_chunks(purchases_csv_path, output_jsons_dir):
    pass


def calculate_unique_clients_from_input(input_path,):
    client_set = set()
    print("calculate_unique_clients_from: {}".format(input_path))
    for df in tqdm(pd.read_csv(input_path, chunksize=500000,)):
        client_set.update(set([row.client_id for row in df.itertuples()]))
    return len(client_set)


def calculate_unique_clients_from_output(output_dir,):
    import glob

    client_cnt = 0
    print("calculate_unique_clients_from: {}".format(output_dir))
    for js_file in glob.glob(output_dir + "/*.jsons"):
        for _ in open(js_file):
            client_cnt += 1
    return client_cnt


if __name__ == "__main__":
    purchases_csv_path = cfg.PURCHASE_CSV_PATH
    output_jsons_dir = cfg.JSONS_DIR

    split_data_to_chunks(purchases_csv_path, output_jsons_dir)

    # check splitting for correctness
    _from_input = calculate_unique_clients_from_input(purchases_csv_path)
    _from_output = calculate_unique_clients_from_output(output_jsons_dir)
    assert _from_input == _from_output
