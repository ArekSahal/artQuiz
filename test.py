from requests_html import HTMLSession
import time
import json
import random
import csv



# Read data

#groups = ["faglar", "daggdjur", "fiskar", "evertebrater", "grod", "svamp", "floristik"]
groups = ["Floristik"]
failed = ["rörsångare", "trädkrypare", "kungsfiskare", "nordisk fladdermus", "varg", "björn", "fjällräv", "järv", "lodjur", "marulk", "pirål", 
"rödhaj", "kolja", "kummel", "hälleflundra", "vattenkvalster", "lockespindel", "enkelfoting", "dubbelfoting", "sötvattensgråsugga", "skinnbaggar", 
"ängsskinnbagge", "skräddare", "skalbaggar", "vivel", "jordlöpare", "dykare", "virvelbagge", "flickslända","dagslända", "nattslända", "parasitstekel",
"bi", "humla", "myra", "gräsfjäril", "harkrank", "stickmygga", "vårtbitare"]

"""
filename: faglar_data.txt

stenskvätta, link1, link2, link3
blåmes, link1, link2
"""



base = "https://artfakta.se"
url = base + "/artbestamning/search/species?q=" # Add search term at the end


def find_animal(name, count): 
    # Use the session above to connect to artfakta.se and search for the input name
    session = HTMLSession()
    resp = session.get(url + name)
    # Run JavaScript code on webpage
    resp.html.render()

    #Takes the first item in the searchbox
    item = resp.html.find("td a")

    if len(item) == 0:
        if count > 2:
            print("giving up on " + name)
            failed.append(name)
            return {"id": None}

        print("failed at finding " + name + ", trying again")
        return find_animal(name, count + 1)

    #From the link return the id (ex: 206026)
    sp_id = item[1].attrs["href"].split("-")[-1]
    return {"id": sp_id, "link": base + item[1].attrs["href"] }

def get_images(name, count):
    #Get the species id from artfakta.se
    species_data = find_animal(name, 0)
    #asyncio.run(species_data)
    session = HTMLSession()

    if species_data["id"]:
        # Post requests that returns json object with image-urls
        response = session.post("https://artfakta.se/api/MediaData/images/taxa/" + species_data["id"] + "?fromChilds=false&source=2&mediaClass=128&validated=null&skip=0&take=12&allImages=true&noOfTaxonImages=5", json={"data": []})
        data = response.json()

        if data["totalCount"] == 0:
            if count > 2:
                print("giving up on " + name)
                failed.append(name)
                return [""]

            print("failed at finding images for " + name + ", trying again")
            return get_images(name, count + 1)
        imgs = []
        items = data["items"]
        for i in items:
            imgs.append(i["exports"][0]["url"])
        return [name] + imgs # Should add copyright info

    else:
        # If we cant find the animal then return None and look for a new one
        # This is also used if the request failed.
        return [""]


def scan_for(group):
    names = []
    with open(group + ".txt", "r", encoding="utf8") as f:
        print("Reading file: " + group + ".txt")
        lines = f.readlines()
        mod_lines = []
        print("Modifing characters")
        for line in lines:
            l = line.replace("Ã¶", "ö")
            l = l.replace("Ã¥", "å")
            l = l.replace("Ã¤", "ä")
            l = l.replace("\n", "")
            mod_lines.append(l)
        names = mod_lines

    for name in names:
        with open(group + ".csv", 'a', newline='', encoding="utf8") as file:
            writer = csv.writer(file)
            print("Getting images for: " + name)
            imgs = get_images(name, 0)
            if imgs[0] != "":
                writer.writerow(imgs)
    print("saved to file: " + group + ".csv")
    print("faield to find: ")
    print(failed)

    return 200
    

def continue_scanning(group):
    names = []
    with open(group + ".txt", "r", encoding="utf8") as f:
        print("Reading file: " + group + ".txt")
        lines = f.readlines()
        mod_lines = []
        print("Modifing characters")
        for line in lines:
            l = line.replace("Ã¶", "ö")
            l = l.replace("Ã¥", "å")
            l = l.replace("Ã¤", "ä")
            l = l.replace("\n", "")
            mod_lines.append(l)
        names = mod_lines
    already_done_names = []
    with open(group + '.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i in csv_reader:
            already_done_names.append(i[0])
    
    for name in names:
        if name in already_done_names:
            pass
        else:
            with open(group + ".csv", 'a', newline='', encoding="utf8") as file:
                writer = csv.writer(file)
                print("Getting images for: " + name)
                imgs = get_images(name, 0)
                if imgs[0] != "":
                    writer.writerow(imgs)
    print("saved to file: " + group + ".csv")
    
    

        
def scan_for_all(cont=False):
    for i in groups:
        if cont:
            continue_scanning(i)
        else:
            scan_for(i)

scan_for_all(cont=True)
#print("fåglar")

