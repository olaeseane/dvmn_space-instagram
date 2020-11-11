import os
from dotenv import load_dotenv
import re
import logging
from instabot import Bot
from PIL import Image


def get_image_files(pattern, dir):
    return filter(lambda x: re.search(pattern, x), os.listdir(dir))


def transform_images(path_to_images):
    image_files = get_image_files("\.jpg|\.png|\.jpeg", path_to_images)
    for image_file in image_files:
        image = Image.open(f"{path_to_images}/{image_file}")
        image.thumbnail((1080, 1080))
        (file_name, _) = os.path.splitext(image_file)
        image.save(
            f"{path_to_images}/{file_name}.jpg", format="JPEG")


def upload_insta_images(path_to_images):
    username = os.getenv("INSTA_USERNAME")
    pwd = os.getenv("INSTA_PASSWORD")
    bot = Bot()
    bot.login(username=username, password=pwd)
    image_files = get_image_files("\.jpg", path_to_images)
    for image_file in image_files:
        bot.upload_photo(f"{path_to_images}/{image_file}",
                         caption="our universe")
        if bot.api.last_response.status_code != 200:
            logging.exception(f"Exception occurred - {bot.api.last_response}")


def main():
    logging.basicConfig(filename="upload_insta.log",
                        level=logging.INFO, filemode="w")
    load_dotenv()
    path_to_images = os.getenv("IMAGE_PATH")

    transform_images(path_to_images)
    upload_insta_images(path_to_images)


if __name__ == "__main__":
    main()
