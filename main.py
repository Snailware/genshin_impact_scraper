
import requests
import time
from bs4 import BeautifulSoup

class Scraper:
# scraper object.

    def __init__(self, url):
        self.base_url           = url
        self.weapon_type_list   = []
        self.weapon_list        = []
        self.character_list     = []
    # initialize variables. 

    def scrapeTypes(self):
        page = requests.get(f"{self.base_url}/Weapons")
        parsed_page = BeautifulSoup(page.content, "html.parser")
        table = parsed_page.find(class_="article-table")
        rough_list = table.find_all("td")
        count = 0
        for weapon in rough_list:
            if count % 2 != 0:
                pass
            else:
                entry = weapon.text
                self.weapon_type_list.append(entry.strip())
            count += 1
    # scrape weapon types.

    def scrapeWeapons(self):
        for weaponType in self.weapon_type_list:

            request_timer = Timer()
            request_timer.start()
            print(f"requesting {weaponType} information...")

            page = requests.get(f"{self.base_url}/{weaponType}")
            request_delay = request_timer.stop()
            print(f"received {weaponType} info in {request_delay} seconds.")
            
            parsed_page = BeautifulSoup(page.content, "html.parser")
            tables = parsed_page.find_all("tbody")
            rows = tables[1].find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                row_entry = []
                for info in cells:
                    entry = info.text.strip()
                    if entry == "":
                        row_entry.append("None")
                    else:
                        row_entry.append(entry.replace("\n", " "))
                if row_entry != []:
                    row_entry.append(weaponType)
                    self.weapon_list.append(row_entry)
    # scrape weapon info, format entries for list and remove junk. 

    def outputWeapons(self):
        tsv_weapon_file = open("weapon_list.tsv", "w")
        tsv_weapon_file.write("name\tweapon type\trarity\tbase attack\t" +
        "2nd stat\tpassive\trank 1\trank 5\n")
        for weapon in self.weapon_list:
            tsv_weapon_file.write(f"{weapon[0]}\t{weapon[8]}\t{weapon[2]}"+
            f"\t{weapon[3]}\t{weapon[4]}\t{weapon[5]}\t{weapon[6]}\t" +
            f"{weapon[7]}\n")
        tsv_weapon_file.close()
    # write table TSV file for viewing / export.

    def scrapeCharacters(self):
        request_timer = Timer()
        request_timer.start()
        print("requesting Character information...")

        page = requests.get(f"{self.base_url}/Characters")
        print(f"received Character info in approx {request_timer.stop()} seconds.")

        parsed_page = BeautifulSoup(page.content, "html.parser")
        table = parsed_page.find_all(class_= "article-table")
        rows = table[1].find_all("tr")
        for row in rows:
            character_entry = []
            cells = row.find_all("td")
            for data in cells:
                if data.text.strip() != "":
                    character_entry.append(data.text.strip())
            if character_entry != []:
                if character_entry[1] == "Traveler":
                    character_entry.append("None")
                self.character_list.append(character_entry)
    # scrape character info from wiki. 

    def outputCharacters(self):
        tsv_character_file = open("character_list.tsv", "w")
        tsv_character_file.write("name\trarity\tgender\tweapon\telement\tnation\n")
        for character in self.character_list:
            tsv_character_file.write(f"{character[1]}\t{character[0]}\t{character[4]}\t{character[3]}\t{character[2]}\t{character[5]}\n")
        tsv_character_file.close()
    # output character info to character list TSV file. 

class Timer:
# timer object.

    def __init__(self):
        pass
    # dont do anything on init.

    def start(self):
        self.start_time = time.time()
    # get starting time. 

    def stop(self):
        self.stop_time = time.time()
        self.elapsed_time = float("{:.2f}".format(self.stop_time - 
                                                    self.start_time))
        return self.elapsed_time
    # get stop time, calculate elapsed time, then return formatted value.

def main():
    
    timer = Timer()
    timer.start()
    print("starting scrape now...")
    # start timer and alert user. 
    
    scraper = Scraper("https://genshin-impact.fandom.com/wiki")
    # create scraper instance.

    scraper.scrapeTypes()
    scraper.scrapeWeapons()
    scraper.outputWeapons()
    # scrape weapon information and output to TSV file.
     
    scraper.scrapeCharacters()
    scraper.outputCharacters()
    # scrape character information and output to TSV file. 

    print(f"execution finished successfully in approx {timer.stop()} seconds.")
    exit()
    # display total execution time then exit program. 

main()