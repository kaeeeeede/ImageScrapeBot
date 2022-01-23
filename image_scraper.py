from bs4 import BeautifulSoup
import requests
import os

folder_name = "Downloads"

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

    for i, image in enumerate(images):
        if link := image.get("data-srcset") or image.get("data-src") or image.get("data-fallback-src") or image.get("src"):
            r = requests.get(link).content
            with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                f.write(r)
                total_file_size += os.path.getsize(f"{folder_name}/images{i+1}.jpg")    
                total_file_number += 1
            if total_file_number < file_count_limit and total_file_size < file_size_limit:
                yield (f"{folder_name}/images{i+1}.jpg")
            else:
                break
        else:
            continue
        
if __name__ == "__main__":
    address = input("Address:- ")
    file_size_limit = input("Size Limit:- ")
    file_count_limit = input("File Limit:- ")
    images = getData(address)
    folder_name = create_folder(images)
    list(download_images(images, folder_name, file_size_limit, file_count_limit))

