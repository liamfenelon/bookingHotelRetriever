
import pandas as pd
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import gzip
import xml.etree.ElementTree as ET

listings = []

url = "https://www.booking.com/sitembk-hotel-index.xml"

def get_Sitemap(url):
    response = urllib.request.urlopen(url)
    xml = BeautifulSoup(response, 
                        'lxml-xml', 
                         from_encoding=response.info().get_param('charset'))

    return xml

xml = get_Sitemap(url)

#for each sitemap, add loc attribute to gzSitemaps

def get_gzSiteMaps(xml):
    
    gzSitemaps = xml.find_all("sitemap")

    ret = []

    for gzSitemap in gzSitemaps:
        ret.append(gzSitemap.findNext("loc").text)
    
    return ret


gzSitemaps = get_gzSiteMaps(xml) # a list of all gz files in the index site map


def openGzFile(url):
    response = urllib.request.urlopen(url)
    with gzip.GzipFile(fileobj=response) as f:
        data = f.read()

    root = ET.fromstring(data)
    
    xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    #print(xml_string)

    return xml_string


firstUrl = 'https://www.booking.com/sitembk-hotel-el.0003.xml.gz'


for gzSite in gzSitemaps:
    xmlString = openGzFile(gzSite)
    root = ET.fromstring(xmlString)
    links = [url.text for url in root.findall('.//{http://www.google.com/schemas/sitemap/0.9}loc')]
    for link in links:
        with open("results.txt", "a") as f:
            f.write(link + "\n")


print("finished")