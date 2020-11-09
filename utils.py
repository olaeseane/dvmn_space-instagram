from pathlib import Path
import requests
import os


def get_extension(url):
    (_, ext) = os.path.splitext(url)
    return ext


def download_image(url, name):
    image_path = os.getenv("IMAGE_PATH")
    Path(image_path).mkdir(parents=False, exist_ok=True)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(f"{image_path}/{name}", "wb") as file:
        file.write(response.content)
        print(f"file {name} was downloaded")
