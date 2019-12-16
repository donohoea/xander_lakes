import os,sys
import requests
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from zipfile import ZipFile

data_path = Path(__file__).parent / 'data'

try:
    os.mkdir(data_path)
except FileExistsError:
    pass

url = 'https://ags.aer.ca/alberta-lake-bathymetry-data.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

success_count = 0
partial_count = 0
fail_count = 0

for lake_link in soup.findAll('a')[59:-22]:
    lake = lake_link.string.strip()
    slug = lake.lower().replace(' ', '+')
    href = f"http://search.aer.ca/ags-en/search/theme/ags?fq%5B%5D=feed%3Aall&fq" \
        "[]=section%3ADigital+Data&q={slug}&sort=relevant"
    path = data_path  / lake

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    response2 = requests.get(href)
    soup2 = BeautifulSoup(response2.text, 'lxml')
    downloads = 0
    for header in soup2.find_all("h4"):
        try:
            if header.a.text.strip().lower().startswith(f'{lake.lower()}, alberta'):
                zip_href = header.parent.div.a['href']
                file_name = path / zip_href[zip_href.find('DIG_'):]
                urllib.request.urlretrieve(zip_href, file_name)
                with ZipFile(file_name, 'r') as zip_file:
                    zip_file.extractall(path=path)
                os.remove(file_name)
                downloads += 1
        except AttributeError:
            pass
    if downloads == 0:
        print(f'No data found for {lake}....')
        fail_count += 1
    elif downloads < 3:
        print(f'Partial data found for {lake}')
        partial_count += 1
    else:
        print(f'{lake} data downloaded....')
        success_count += 1
print('----------------------------------------')
print('Scrape Complete')
print(f'Downloaded data for {success_count} lakes')
print(f'No Data was found for {fail_count} lakes')
