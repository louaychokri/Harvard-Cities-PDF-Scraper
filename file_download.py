from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os
import time
 

class Download:
    def __init__(self):
        
        self.download_dir = os.path.join(os.getcwd(), "downloads") 
        os.makedirs(self.download_dir, exist_ok=True)

        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/129.0.0.0 Safari/537.36"
        )

        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        }
        self.chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.url = "https://growthlab.hks.harvard.edu/publications/policy-area/citiesregions"
        self.driver.get(self.url)

        self.cities_url = []
    

    def scroll_page(self):
        print("Starting page scroll...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def get_cities_in_page(self):
        self.scroll_page()
        body = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
        print("All URLs find")
        cities = body.find_elements(By.CLASS_NAME, "clearfix")
        for i, citie in enumerate(cities):
            href = citie.find_element(By.TAG_NAME, "a")
            citie_url = href.get_attribute("href")
            self.cities_url.append(citie_url)
            print(f"Url number :{i}, URL :{citie_url}")

            
    def get_next_page(self): 
        page = 0
        while True:  
            scraper.driver.get(f"https://growthlab.hks.harvard.edu/publications/policy-area/citiesregions?page={page}")
            button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pager-next")))
            link = button.find_element(By.TAG_NAME,"a")
            href = link.get_attribute("href")
            link.click()
            print(f"Navigated to page :{page}")
            page+=1
            return True


    def wait_for_download(self, timeout=60):
        """Wait for the download to complete by checking for .crdownload files."""
        seconds = 0
        while seconds < timeout:
            time.sleep(1)
            downloading = any(f.endswith('.crdownload') for f in os.listdir(self.download_dir))
            if not downloading:
                print("Download completed.")
                return True
            seconds += 1
        print("Download timeout exceeded.")
        return False


    def get_doc_from_citie(self):
        self.scroll_page()
        i = 0
        for href in self.cities_url:
            try:  
                self.driver.get(href)
                download = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "biblio-upload-wrapper")))
                file = download.find_elements(By.TAG_NAME, "a")  
                for hrefs in file:
                    download_link = hrefs.get_attribute("href")
                    print(f"Download file :{i}, was find :{download_link}")
                    i+=1
                    hrefs.click()
                    if not self.wait_for_download():
                            print(f"Warning: Download for {download_link} may not have completed.")
            except TimeoutException:
                print("Download element NOT found, skipping...")


    def close(self):
        self.driver.quit()
        print("WebDriver closed.")


if __name__ == "__main__":
    scraper = None 
    while True: 
        try:
            scraper = Download()    
            scraper.get_cities_in_page()
            scraper.get_doc_from_citie()
            if not scraper.get_next_page():
                break
        except Exception as e:
            print(f"Error in main: {e}")
        finally:
            if scraper:
                scraper.close()
