# Space Instagram

Auto uploading pictures for instagramm account

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
After setup environment variables in `.env` file
```
INSTA_USERNAME=instagram username
INSTA_PASSWORD=instagram password
IMAGE_PATH=path for image downloading
```

### How to run

A. Fetch images from SpaceX and Hubble
```
python fetch_spacex.py
python fetch_hubble.py
```
B. Upload fetched images on Instagram
```
python upload_insta.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).