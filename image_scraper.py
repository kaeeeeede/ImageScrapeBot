from bs4 import BeautifulSoup
import requests
import os

folder_name = "Downloads"

def create_folder(images):
    try:
        os.mkdir(folder_name)
    except:
        pass
    download_images(images, folder_name)

def download_images(images, folder_name):
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_link = image["data-srcset"]
            except:
                try:
                    image_link = image["data-src"]
                except:
                    try:
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            image_link = image["src"]
                        except:
                            pass
            try:
                r = requests.get(image_link).content
                try:
                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                        f.write(r)
            except:
                pass

def getData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    create_folder(images)