from requests_html import HTMLSession
import time
import json
import random

base = "https://artfakta.se"
sok = "rödräv"
url = base + "/artbestamning/search/species?q="
 
# create an HTML Session object
session = HTMLSession()
#session.post(base, cookies={"ADBMediaSource": "2"},headers = {'User-Agent': 'Mozilla/5.0'})
#print(session.cookies.keys())

def find_animal(name):
    
    # Use the object above to connect to needed webpage
    resp = session.get(url + name)
    
    # Run JavaScript code on webpage
    resp.html.render()

    item = resp.html.find("td a")

    return item[1].attrs["href"][-6:]

def get_image(name):
    species_id = find_animal(name)

    response = session.post("https://artfakta.se/api/MediaData/images/taxa/" + species_id + "?fromChilds=false&source=2&mediaClass=128&validated=null&skip=0&take=12&allImages=true&noOfTaxonImages=5", json={"data": []})
    items = response.json()["items"]
    element = random.choice(items)
    return element["exports"][0]["url"]

print(get_image("vitsippa"))
#print("It worked.. It FUKCING WORKED!")
