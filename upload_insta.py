import os
from instabot import Bot
from PIL import Image
from instabot.api.api_photo import compatible_aspect_ratio, get_image_size
from dotenv import load_dotenv
import utils


def crop_maximize_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):
    from scipy.optimize import minimize_scalar
    import numpy as np

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
    files = filter(lambda x: '.' in x, os.listdir(utils.IMAGE_DIR))
    for f in files:
        try:
            if not compatible_aspect_ratio(get_image_size(f"{utils.IMAGE_DIR}/{f}")):
                image = Image.open(f"{utils.IMAGE_DIR}/{f}")
                image = crop_maximize_entropy(image)
                image.save(utils.IMAGE_DIR+"/"+f.split(".")[0]+".jpg", format="JPEG")
        except Exception as err:
            pass


def upload_insta_images():
    load_dotenv()
    username = os.getenv("INSTA_USERNAME")
    pwd = os.getenv("INSTA_PASSWORD")
    bot = Bot()
    bot.login(username=username, password=pwd)
    files = filter(lambda x: '.jpg' in x, os.listdir(utils.IMAGE_DIR))
    for f in files:
        bot.upload_photo(utils.IMAGE_DIR+"/"+f, caption="our universe")
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)


def main():
    try:
        transform_images()
        upload_insta_images()
    except Exception as err:
        print(f"Error occured - {err}")


if __name__ == "__main__":
    main()
