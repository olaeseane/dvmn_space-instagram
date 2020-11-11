from pathlib import Path
import requests
import os
from dotenv import load_dotenv


def download_image(url, name):
    load_dotenv()
    path_to_images = os.getenv("IMAGE_PATH")
    Path(path_to_images).mkdir(parents=False, exist_ok=True)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(f"{path_to_images}/{name}", "wb") as file:
        file.write(response.content)
        print(f"file {name} was downloaded")
