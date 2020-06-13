from requests_html import HTMLSession
import time
import json
import random

base = "https://artfakta.se"
url = base + "/artbestamning/search/species?q=" # Add search term at the end
 
# create an HTML Session object
session = HTMLSession()

def find_animal(name): 
    # Use the session above to connect to artfakta.se and search for the input name
    resp = session.get(url + name)
    # Run JavaScript code on webpage
    resp.html.render()

    #Takes the first item in the searchbox
    item = resp.html.find("td a")

    if len(item) == 0:
        return None

    #From the link return the id (ex: 206026)
    return {"id": item[1].attrs["href"][-6:], "link": base + item[1].attrs["href"] }

def get_image(name):
    #Get the species id from artfakta.se
    species_data = find_animal(name)

    if species_data["id"]:
        response = session.post("https://artfakta.se/api/MediaData/images/taxa/" + species_data["id"] + "?fromChilds=false&source=2&mediaClass=128&validated=null&skip=0&take=12&allImages=true&noOfTaxonImages=5", json={"data": []})
        data = response.json()
        if data["totalCount"] == 0:
            return None
        items = data["items"]
        element = random.choice(items)
        return {"img": element["exports"][0]["url"], "link": species_data["link"]}

    else:
        # If we cant find the animal then return None and look for a new one
        # This is also used if the request failed.
        return None

print(get_image("hermelin"))
#print("It worked.. It FUKCING WORKED!")
