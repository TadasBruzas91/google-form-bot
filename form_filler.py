from web_scraper import Scraper
from selenium.webdriver.common.by import By

class Form(Scraper):
    def __init__(self, driver_path="", browser_options=[], base_url=""):
        super().__init__(driver_path, browser_options, base_url)


    def find_inputs(self, input_titles_for_test):
        self.inputs = self.browser.find_elements(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader")
        if self.inputs:
            self.check_inputs(input_titles_for_test)
            pass

    def check_inputs(self, input_titles_for_test):
        for index, input in enumerate(self.inputs):
            if input.text != input_titles_for_test[index]:
                print(f"Incorrect title found '{input.text}' required '{input_titles_for_test[index]}'")
                return
        print("Form check success!")

if __name__ == "__main__":
    from python_json_config import ConfigBuilder
    builder = ConfigBuilder()
    config = builder.parse_config("./config.json")

    form = Form(config.webdriver.driver_path, config.webdriver.options, config.form.url)
    form.find_inputs(config.form.input_titles)