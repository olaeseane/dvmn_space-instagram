import requests
import urllib3
import logging
import utils


SPACEX_LATEST_API = "https://api.spacexdata.com/v4/launches/latest"
SPACEX_API = "https://api.spacexdata.com/v4/launches"


def fetch_spacex_last_launch():
    response = requests.get(SPACEX_LATEST_API)
    response.raise_for_status()
    response_list = response.json()
    if not response_list["links"]["flickr"]["original"]:
        response = requests.get(SPACEX_API)
        response_list = response.json()
        for launch in response_list:
            if launch["links"]["flickr"]["original"]:
                spacex_image = launch["links"]["flickr"]["original"]
                break
    for num_image, url_image in enumerate(spacex_image):
        utils.download_image(url_image, f"spacex{num_image}.jpg")


def main():
    logging.basicConfig(filename="fetch_spacex.log",
                        level=logging.INFO, filemode="w")
    try:
        urllib3.disable_warnings()
        fetch_spacex_last_launch()
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Error occured - {conn_err}")


if __name__ == "__main__":
    main()
