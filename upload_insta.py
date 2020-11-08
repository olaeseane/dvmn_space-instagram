import os
from dotenv import load_dotenv
import re
import logging
from instabot import Bot
from PIL import Image
import utils


def get_image_files(pattern, dir):
    return filter(lambda x: re.search(pattern, x), os.listdir(dir))


def transform_images():
    image_files = get_image_files("\.jpg|\.png|\.jpeg", utils.IMAGE_DIR)
    for image_file in image_files:
        image = Image.open(f"{utils.IMAGE_DIR}/{image_file}")
        image.thumbnail((1080, 1080))
        image.save(
            f"{utils.IMAGE_DIR}/{image_file.split('.')[0]}.jpg", format="JPEG")


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
