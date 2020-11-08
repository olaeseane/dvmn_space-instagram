import requests
import os
import urllib3
import utils


HUBBLE_IMAGE_API = "http://hubblesite.org/api/v3/image/"
HUBBLE_COLLECTION_API = "http://hubblesite.org/api/v3/images/"
HUBBLE_COLLESTIONS = ["holiday_cards", "wallpaper",
                      "spacecraft", "news", "printshop", "stsci_gallery"]


def fetch_hubble_image(image_id):
    response = requests.get(HUBBLE_IMAGE_API+str(image_id))
    response.raise_for_status()
    response_list = response.json()
    url = f"https:{response_list['image_files'][-1]['file_url']}"
    name = f"{str(image_id)}.{utils.get_extension(url)}"
    utils.download_image(url, name)


def fetch_hubble_collection(collection):
    response = requests.get(HUBBLE_COLLECTION_API+collection)
    response.raise_for_status()
    response_list = response.json()
    for image in response_list:
        fetch_hubble_image(image["id"])


def main():
    try:
        urllib3.disable_warnings()
        fetch_hubble_collection(HUBBLE_COLLESTIONS[4])
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error occured - {conn_err}")


if __name__ == "__main__":
    main()
