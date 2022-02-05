from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd


class Scraper():
    def __init__(self, driver_path="", browser_options=[], base_url=""):
        print(base_url)

        self.set_browser_options(driver_path, browser_options)

        if "chromedriver" in driver_path:
            if self.options:
                ser = Service(driver_path)
                self.browser = webdriver.Chrome(service=ser,options=self.options)

        if self.browser:
            self.browser.get(base_url)


    def set_browser_options(self, driver_path, options):
        if "chromedriver" in driver_path:
            self.options = webdriver.ChromeOptions()
        
        if self.options:
            for option in options:
                self.options.add_argument(option)

    def go_to_address(self, address):
        if self.browser:
            self.browser.implicitly_wait(10)
            self.search_input = self.browser.find_element(By.ID,"txtSearchInput")
            if self.search_input:
                self.search_input.clear()
                self.search_input.send_keys(address)
                self.search_input.send_keys(Keys.ENTER)
                
    def got_to_out_transactions(self):
        if self.browser:
            self.browser.implicitly_wait(10)
            self.view_filter = self.browser.find_element(By.ID, "ddlTxFilter")
            if self.view_filter:
                self.view_filter.click()
            
            self.out_transactions = self.browser.find_element(By.LINK_TEXT, "View Completed Txns")
            if self.out_transactions:
                self.out_transactions.click()
            
            self.records_size = Select(self.browser.find_element(By.ID, "ContentPlaceHolder1_ddlRecordsPerPage"))
            if self.records_size:
                self.records_size.select_by_visible_text("100")

    def save_table_data(self):
        if self.browser:
            self.table = self.browser.find_element(By.TAG_NAME, "table")
            self.data = pd.read_html(self.table.get_attribute('outerHTML'))

            self.time_converter()
            self.value_converter()
            print(self.data[0]["To"])
        
    def time_converter(self):
        if self.data:
            for index, time in enumerate(self.data[0]["Age"]):
                time_list = time.split(" ")
                minutes = 0
                if time_list[1].lower() == "min" or time_list[1].lower() == "mins":
                    minutes = int(time_list[0])
                elif time_list[1].lower() == "hr" or time_list[1].lower() == "hrs":
                    minutes = int(time_list[0]) * 60 + int(time_list[2])
                elif time_list[1].lower() == "day" or time_list[1].lower() == "days":
                    minutes = int(time_list[0]) * 1440 + int(time_list[2]) * 60
                self.data[0]["Age"][index] = minutes

    def value_converter(self):
        for index, value in enumerate(self.data[0]["Value"]):
                value_list = value.split(" ")
                self.data[0]["Value"][index] = float(value_list[0])






# For testing
if __name__ == "__main__":
    from python_json_config import ConfigBuilder
    builder = ConfigBuilder()
    config = builder.parse_config("./config.json")
    scraper = Scraper(config.webdriver.driver_path, config.webdriver.options, config.scraper.base_url)
    scraper.go_to_address(config.scraper.address)
    scraper.got_to_out_transactions()
    scraper.save_table_data()