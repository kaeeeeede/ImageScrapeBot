from bs4 import BeautifulSoup
import requests
import os

folder_name = "Downloads"
img = []

def getData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    create_folder(images)

def create_folder(images):
    try:
        os.mkdir(folder_name)
    except:
        pass
    download_images(images, folder_name)

def download_images(images, folder_name):
    if len(images) != 0:
        for i, image in enumerate(images):
            if image.get("data-srcset") != None:
                image_link = image["data-srcset"]
            elif image.get("data-src") != None:
                image_link = image["data-src"]
            elif image.get("data-fallback-src") != None:
                image_link = image["data-fallback-src"]
            elif image.get("src") != None:
                image_link = image["src"]
            else:
                continue

            r = requests.get(image_link).content
            with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                f.write(r)
                img.append(f"{folder_name}/images{i+1}.jpg")

    return(img)

if __name__ == "__main__":
    address = input("Address:- ")
    getData(address)
