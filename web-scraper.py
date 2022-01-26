from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Scraper():
    def __init__(self, driver_path="", browser_options=[], base_url=""):
        print(base_url)

        self.set_browser_options(driver_path, browser_options)

        if "chromedriver" in driver_path:
            if self.options:
                self.browser = webdriver.Chrome(executable_path=driver_path,options=self.options)

        if self.browser:
            self.browser.get(base_url)


    def set_browser_options(self, driver_path, options):
        if "chromedriver" in driver_path:
            self.options = webdriver.ChromeOptions()
        
        if self.options:
            for option in options:
                self.options.add_argument(option)



if __name__ == "__main__":
    from python_json_config import ConfigBuilder
    builder = ConfigBuilder()
    config = builder.parse_config("./config.json")
    scraper = Scraper(config.webdriver.driver_path, config.webdriver.options, config.scraper.base_url)