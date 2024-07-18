import argparse
import glob
import os
import shutil
import yaml

from PIL import Image

from utils.find_project_root import find_project_root

def resize_images_in_directory(source_path: str, destination_path: str, resolution_x: int = 512, resolution_y: int = 512) -> None:

    if not destination_path.exists():
        destination_path.mkdir(parents=True)
    else:
        shutil.rmtree(destination_path)
        destination_path.mkdir(parents=True)

    for file_path in glob.iglob(str(source_path) + "/" + '**/*.jpg', recursive=True):

        destination_file_path = file_path.replace(str(source_path), str(destination_path))
        subdirectory_path = os.path.dirname(destination_file_path)
        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)

        image = Image.open(file_path)
        resized = image.resize((resolution_x, resolution_y))
        resized.save(destination_file_path)

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--params', dest='params', required=True)
    args = args_parser.parse_args()

    with open(args.params) as param_file:
        params = yaml.safe_load(param_file)

    PROJECT_ROOT = find_project_root()
    IMAGE_RESOLUTION: int = params['resize_images']['resolution']

    source_path = PROJECT_ROOT / "data/external/lego"
    destination_path = PROJECT_ROOT / "data/processed/lego"

    resize_images_in_directory(source_path, destination_path, IMAGE_RESOLUTION, IMAGE_RESOLUTION)
    