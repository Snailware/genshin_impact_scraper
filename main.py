
# program will scrape genshin impact wiki for weapon info and create tsv file.

import requests
import time
from bs4 import BeautifulSoup

def main():

    timer = VerboseTimer()
    timer.start()
    # create verbose timer object and begin timing. 

###############################################################################

    weapon_types = weaponTypeGetter()
    # get weapon types list from weapon page.

    weaponDataFill(weapon_types)








###############################################################################

    timer.stop()
    exit()


class VerboseTimer:
# timer object that will print output independantly.

    def __init__(self):
        pass
    # dont do anything on init.

    def start(self):
        self.start_time = time.time()
        print("starting timer...")
    # get starting time and print notification. 

    def stop(self):
        self.stop_time = time.time()
        self.elapsed_time = self.stop_time - self.start_time
        print("execution completed in approx {:.2f} seconds." \
            .format(self.elapsed_time))
    # get stop time, calculate elapsed time, then display. 

    weapon_types = weaponTypeGetter()
    # get weapon types list from weapon page.

def weaponDataFill(weapon_types):

    for weapon_type in weapon_types:

        type_page = pageParser(weapon_type)
        print(f"requesting {weapon_type} page...")

        




def weaponTypeGetter():
# get weapon types and return list. 

    type_list = []
    # create list for types. 

    weapon_page = pageParser("Weapons")
    # navigate to weapons/table page for master weapon list. 

    type_table = weapon_page.find(class_="article-table")
    rough_list = type_table.find_all("td")
    # navigate to table and find all entries.

    count = 0
    for weapon in rough_list:
        if count % 2 != 0:
            pass
        else:
            entry = weapon.text
            type_list.append(entry.strip())
        count += 1
    # iterate through data, only adding every other entry.

    return type_list
    # return list.

def pageParser(page_url):
# encode url, request page, parse results, then return object.

    requestTimer = VerboseTimer
    base_url = "https://genshin-impact.fandom.com/wiki"
    new_url = f"{base_url}/{page_url}"
    # combine and encode base and page url.

    page = requests.get(new_url)
    parsed_page = BeautifulSoup(page.content, "html.parser")
    return parsed_page
    # request page from created url, parse object with html parser and return
    # parsed page object. 

main()