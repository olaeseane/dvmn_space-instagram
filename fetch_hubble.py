import requests
import urllib3
import logging
import utils
from dotenv import load_dotenv
import os


HUBBLE_IMAGE_API = "http://hubblesite.org/api/v3/image/"
HUBBLE_COLLECTION_API = "http://hubblesite.org/api/v3/images/"
HUBBLE_COLLESTIONS = {"holiday_cards": "holiday_cards", "wallpaper": "wallpaper",
                      "spacecraft": "spacecraft", "news": "news", "printshop": "printshop", "stsci_gallery": "stsci_gallery"}


def fetch_hubble_image(image_id):
    response = requests.get(f"{HUBBLE_IMAGE_API}{image_id}")
    response.raise_for_status()
    image_data = response.json()
    url = f"https:{image_data['image_files'][-1]['file_url']}"
    (_, ext) = os.path.splitext(url)
    name = f"{image_id}{ext}"
    utils.download_image(url, name)


def fetch_hubble_collection(collection):
    response = requests.get(f"{HUBBLE_COLLECTION_API}{collection}")
    response.raise_for_status()
    image_collection = response.json()
    for image in image_collection:
        fetch_hubble_image(image["id"])


def main():
    load_dotenv()
    logging.basicConfig(filename="fetch_hubble.log",
                        level=logging.INFO, filemode="w")
    try:
        urllib3.disable_warnings()
        fetch_hubble_collection(HUBBLE_COLLESTIONS["stsci_gallery"])
    except requests.exceptions.ConnectionError as conn_err:
        logging.exception(f"Exception occured - {conn_err}")
    except requests.exceptions.HTTPError as http_err:
        logging.exception(f"Exception occured - {http_err}")


if __name__ == "__main__":
    main()
