from bs4 import BeautifulSoup
import requests
import os
import utils
import shutil

def getData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    
    return images

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def get_image_link_from_tag(tag):
    possible_sources = ["data-srcset", "data-src", "data-fallback-src", "src"]

    for source in possible_sources:
        if not (link := tag.get(source)):
            continue

        return link

def cleanup(folder_name):
    shutil.rmtree(folder_name, ignore_errors = True)

def download_images(url, file_size_limit, file_count_limit, folder_name = "Downloads", cleanup_before_downloading = True):
    total_file_size = 0
    total_file_number = 0

    if cleanup_before_downloading:
        cleanup(folder_name)

    images = getData(url)
    create_folder(folder_name)

    for i, image in enumerate(images):
        if not get_image_link_from_tag(image):
            continue
        link = get_image_link_from_tag(image)
        r = requests.get(link).content
        with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
            f.write(r)
            total_file_size += utils.get_filesize_mb(f"{folder_name}/images{i+1}.jpg")    
            total_file_number += 1
        
        if not total_file_number > file_count_limit and total_file_size > file_size_limit:
            break
        
        yield (f"{folder_name}/images{i+1}.jpg")

if __name__ == "__main__":
    address = input("Address:- ")
    file_size_limit = int(input("Size Limit:- "))
    file_count_limit = int(input("File Limit:- "))
    list(download_images(address, file_size_limit, file_count_limit))

