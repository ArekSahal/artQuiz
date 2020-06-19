import csv
from random import choice

groups = ["faglar", "daggdjur", "fiskar"]

data = {}


def read_group(group):
    group_sub = []
    with open(group + '.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            l = row[0]
            l = l.replace("Ã¶", "ö")
            l = l.replace("Ã¥", "å")
            l = l.replace("Ã¤", "ä")
            l = l.replace("\n", "")
            row[0] = l

            group_sub.append(row)
    data[group] = group_sub
    return None

def get_all_groups():
    for i in groups:
        read_group(i)
    print("got all groups")

def get_img(grps):
    big_list = []
    for i in grps:
        big_list = big_list + data[i]
    species = choice(big_list)
    img = choice(species[1:])
    return [species[0], img]


get_all_groups()