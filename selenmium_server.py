from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SeleniumServer:
    def __init__(self, server_url=r'C:\Users\sanid\Downloads\chromedriver-win64\chromedriver-win64\chromedriver'):
        self.server_url = server_url
        self.driver = webdriver.Chrome()
        

    def initialize_driver(self,locality,city):
        self.driver.get("https://www.magicbricks.com/")
        time.sleep(10)
        elem = self.driver.find_element(By.CLASS_NAME, "mb-search__title")
        self.driver.execute_script("arguments[0].click();", elem)
        input_span = self.driver.find_element(By.ID, "rent_budget_lbl")  
        self.driver.execute_script("arguments[0].innerText = 'Greater than 5-Lacs';", input_span)
    
        search_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="keyword"]')))
        query = f"{locality}, {city}"
        banglore = self.driver.find_element(By.CLASS_NAME,'mb-search__tag-close')
        self.driver.execute_script("arguments[0].click();", banglore)
    
        for char in query:
            search_box.send_keys(char)
            time.sleep(1) 

        suggestions = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mb-search__auto-suggest__item")))
        suggestions[0].click()

        self.driver.find_elements(By.XPATH, '//*[@id="searchFormHolderSection"]/section/div/div[1]/div[3]/div[4]')[0].click()

data = SeleniumServer()
data.initialize_driver("Sector 17", "Noida")        
                                            
         