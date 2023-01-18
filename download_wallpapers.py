import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from sys import argv

page = 1
links = []
script, input_date, resolution = argv


def download(url, date):
    path = "download\\" + date
    if not os.path.isdir(path):
        os.makedirs(path)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(path, url.split("/")[-1])
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True,
                    unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))


while True:
    if page == 1:
        request = requests.get("https://www.smashingmagazine.com/category/wallpapers/")
    else:
        request = requests.get("https://www.smashingmagazine.com/category/wallpapers/page/" + str(page) + "/")
    soup = bs(request.text, "html.parser")
    article_links = soup.find_all("h2", class_="article--post__title h1")

    if len(article_links):
        for link in article_links:
            link = str(link.find("a"))
            tmp_list = link.split("/")
            tmp_link = "https://www.smashingmagazine.com/" + tmp_list[1] + "/" + tmp_list[2] + "/" + tmp_list[3] + "/"
            tmp_date = tmp_list[1] + tmp_list[2]
            links.append((tmp_date, tmp_link))
        page += 1
    else:
        break

inList = False
for i in links:
    if i[0] == input_date:
        inList = True
        request = requests.get(i[1])
        soup = bs(request.text, "html.parser")
        img_links = soup.find_all("a", string="1920x1080")
        for link in img_links:
            download_link = link.get('href')
            download(download_link, input_date)
if not inList:
    print("Not found!")
