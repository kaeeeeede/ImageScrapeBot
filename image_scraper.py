from bs4 import BeautifulSoup
import requests
import os

folder_name = "Downloads"
img = []

def getData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    
    return images

def create_folder(images):
    try:
        os.mkdir(folder_name)
    except:
        pass
    
    return folder_name

def download_images(images, folder_name, file_size_limit, file_count_limit):
    total_file_size = 0
    total_file_number = 0

    while total_file_size < file_size_limit and total_file_number < file_count_limit:
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
                total_file_size += os.path.getsize(f"{folder_name}/images{i+1}.jpg")
                total_file_number += 1
                if total_file_size < file_size_limit and total_file_number < file_count_limit:
                    img.append(f"{folder_name}/images{i+1}.jpg")
                else:
                    break

    return img

if __name__ == "__main__":
    address = input("Address:- ")
    getData(address)