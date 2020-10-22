
import requests
import time
from bs4 import BeautifulSoup

class Scraper:
# scraper object.

    def __init__(self, url):
        self.base_url = url
        self.weapon_type_list = []
        self.weapon_list = []
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
        tsv_weapon_file = open("weapon_list.tsv", "a")
        tsv_weapon_file.write("name\tweapon type\trarity\tbase attack\t" +
        "2nd stat\tpassive\trank 1\trank 5\n")
        for weapon in self.weapon_list:
            tsv_weapon_file.write(f"{weapon[0]}\t{weapon[8]}\t{weapon[2]}"+
            f"\t{weapon[3]}\t{weapon[4]}\t{weapon[5]}\t{weapon[6]}\t" +
            f"{weapon[7]}\n")
        tsv_weapon_file.close()
    # write table TSV file for viewing / export.

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
    scraper.scrapeTypes()
    scraper.scrapeWeapons()
    scraper.outputWeapons()
    # scrape weapon information and output to TSV file. 

    print(f"execution finished successfully in approx {timer.stop()} seconds.")
    exit()
    # display total execution time then exit program. 

main()