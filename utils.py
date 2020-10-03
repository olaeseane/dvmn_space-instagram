from pathlib import Path
import requests


IMAGE_DIR = "images"


def get_extension(url):
    return url.split(".")[-1]


def download_image(url, name):
    Path(IMAGE_DIR).mkdir(parents=False, exist_ok=True)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(f"{IMAGE_DIR}/{name}", "wb") as file:
        file.write(response.content)
        print(f"file {name} was downloaded")
