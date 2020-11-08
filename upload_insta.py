import os
from dotenv import load_dotenv
import re
import logging
from instabot import Bot
from instabot.api.api_photo import compatible_aspect_ratio, get_image_size
from PIL import Image
from scipy.optimize import minimize_scalar
import numpy as np
import utils


def get_image_files(pattern, dir):
    return filter(lambda x: re.search(pattern, x), os.listdir(dir))


def crop_maximize_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):

    def _entropy(data):
        """Calculate the entropy of an image"""
        hist = np.array(Image.fromarray(data).histogram())
        hist = hist / hist.sum()
        hist = hist[hist != 0]
        return -np.sum(hist * np.log2(hist))

    def crop(x, y, data, w, h):
        x = int(x)
        y = int(y)
        return data[y: y + h, x: x + w]

    w, h = img.size
    data = np.array(img)
    ratio = w / h
    if ratio > max_ratio:  # Too wide
        w_max = int(max_ratio * h)

        def _crop(x):
            return crop(x, y=0, data=data, w=w_max, h=h)

        xy_max = w - w_max
    else:  # Too narrow
        h_max = int(w / min_ratio)

        def _crop(y):
            return crop(x=0, y=y, data=data, w=w, h=h_max)

        xy_max = h - h_max

    def to_minimize(xy): return -_entropy(_crop(xy))  # noqa: E731
    x = minimize_scalar(to_minimize, bounds=(0, xy_max), method="bounded").x
    return Image.fromarray(_crop(x))


def transform_images():
    image_files = get_image_files("\.jpg|\.png|\.jpeg", utils.IMAGE_DIR)
    for image_file in image_files:
        try:
            if not compatible_aspect_ratio(get_image_size(f"{utils.IMAGE_DIR}/{image_file}")):
                image = Image.open(f"{utils.IMAGE_DIR}/{image_file}")
                image.thumbnail((1080, 1080))
                image.save(
                    f"{utils.IMAGE_DIR}/{image_file.split('.')[0]}.jpg", format="JPEG")
        except Exception as err:
            pass


def upload_insta_images():
    username = os.getenv("INSTA_USERNAME")
    pwd = os.getenv("INSTA_PASSWORD")
    bot = Bot()
    bot.login(username=username, password=pwd)
    image_files = get_image_files("\.jpg", utils.IMAGE_DIR)
    for image_file in image_files:
        bot.upload_photo(f"{utils.IMAGE_DIR}/{image_file}",
                         caption="our universe")
        if bot.api.last_response.status_code != 200:
            logging.error(bot.api.last_response)


def main():
    logging.basicConfig(filename="upload_insta.log",
                        level=logging.INFO, filemode="w")
    load_dotenv()
    transform_images()
    upload_insta_images()


if __name__ == "__main__":
    main()
