import argparse
import base64
import io
import logging
import os
import requests
import shutil
import yaml
import zipfile

from pathlib import Path

from utils.find_project_root import find_project_root

if __name__ == '__main__':

    #0: Set up parameters and configure logging level
    logging.basicConfig(
        level=os.environ.get('LOGLEVEL', 'INFO').upper()
    )

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--params', dest='params', required=True)
    args = args_parser.parse_args()

    with open(args.params) as param_file:
        params = yaml.safe_load(param_file)

    PROJECT_ROOT = find_project_root()
    DATASET_VERSION: str = params['download_data']['dataset_version']

    #1: Preparing the URL.
    base_url = "https://www.kaggle.com/api/v1"
    owner_slug = "ihelon"
    dataset_slug = "lego-minifigures-classification"

    url = f"{base_url}/datasets/download/{owner_slug}/{dataset_slug}?datasetVersionNumber={DATASET_VERSION}"

    #2: Encoding the credentials and preparing the request header.
    username = os.environ['KAGGLE_USERNAME']
    key = os.environ['KAGGLE_KEY']
    creds = base64.b64encode(bytes(f"{username}:{key}", "ISO-8859-1")).decode("ascii")
    headers = {
    "Authorization": f"Basic {creds}"
    }

    #3: Sending a GET request to the URL with the encoded credentials.
    response = requests.get(url, headers=headers)

    #4: Loading the response as a file via io and opening it via zipfile.
    zf = zipfile.ZipFile(io.BytesIO(response.content))

    #5: Create directory or empty existing
    save_path = PROJECT_ROOT / "data/external/lego"

    if not save_path.exists():
        save_path.mkdir(parents=True)
    else:
        shutil.rmtree(save_path)
        save_path.mkdir(parents=True)

    #6: Save zip file to directory
    zf.extractall(path=save_path)
    logging.info(f"Wrote Kaggle dataset to {save_path}")