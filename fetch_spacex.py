import requests
import os
import urllib3
import utils


SPACEX_API = "https://api.spacexdata.com/v4/launches/latest"


def fetch_spacex_last_launch():
    response = requests.get(SPACEX_API)
    response.raise_for_status()
    response_json = response.json()
    if not response_json["links"]["flickr"]["original"]:
        response = requests.get(SPACEX_API[:-7])
        response_json = response.json()
        for launch in response_json:
            if launch["links"]["flickr"]["original"]:
                spacex_images = launch["links"]["flickr"]["original"]
                break
    for num_image, url_image in enumerate(spacex_images):
        utils.download_image(url_image, f"spacex{num_image}.jpg")


def main():
    try:
        urllib3.disable_warnings()
        fetch_spacex_last_launch()
    except Exception as err:
        print(f"Error occured - {err}")


if __name__ == "__main__":
    main()
