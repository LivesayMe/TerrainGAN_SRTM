def get_links():
    import urllib.request
    opener = urllib.request.FancyURLopener({})
    url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/SRTMGL1_page_1.html"
    f = opener.open(url)
    content = f.read()
    content = str(content)
    import re
    link_regex = re.compile(r'(<a href="[\w\d://\.]+jpg">)')
    matches = re.findall(link_regex, content)
    links = [x.split('"')[1] for x in matches]


    #Write links to csv file
    import csv
    with open('links.csv', 'w') as f:
        writer = csv.writer(f)
        for l in links:
            writer.writerow([l])


#Process Image
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

path = "N00E009.SRTMGL1.2.jpg"
chunk_folder = "./chunks"
img = Image.open(path)

def get_chunks(img, chunk_size):
    w, h = img.size
    for i in range(0, h, chunk_size):
        for j in range(0, w, chunk_size):
            # Check if chunk is within image
            if i + chunk_size > h or j + chunk_size > w:
                continue
            else:
                box = (j, i, j+chunk_size, i+chunk_size)
                yield img.crop(box)

def is_chunk_interesting(img):
    #See if standard deviation of image is outside of threshold
    threshold = 5
    std = np.std(img)
    print(std)
    return std > threshold

def process_image(img, num):
    chunk_size = 500
    target_size = 500
    chunks = get_chunks(img, chunk_size)
    for i, chunk in enumerate(chunks):
        # plt.imshow(chunk)
        # plt.show()
        chunk = chunk.resize((target_size, target_size), Image.ANTIALIAS)
        if is_chunk_interesting(chunk):
            #Save chunk to folder
            chunk.save(os.path.join(chunk_folder, str(num) + "_" + str(i) + ".jpg"))

# process_image(img)

#Process all images in SRTM folder
srtm_folder = "./SRTM"
for i, f in enumerate(os.listdir(srtm_folder)):
    path = os.path.join(srtm_folder, f)
    img = Image.open(path)
    process_image(img, i)