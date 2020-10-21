
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
            


    # scrape weapons from weapon type pages. 

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
    
    scraper = Scraper("https://genshin-impact.fandom.com/wiki")
    scraper.scrapeTypes()
    scraper.scrapeWeapons()



    elapsed_time = timer.stop()
    print(f"execution finished successfully in approx {elapsed_time} seconds.")










    



main()