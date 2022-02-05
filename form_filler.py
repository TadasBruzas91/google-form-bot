from web_scraper import Scraper
from selenium.webdriver.common.by import By
from time import sleep

class Form(Scraper):
    def __init__(self, driver_path="", browser_options=[], base_url=""):
        super().__init__(driver_path, browser_options, base_url)


    def find_inputs(self, input_titles_for_test):
        self.inputs = self.browser.find_elements(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseRoot")
        if self.inputs:
            self.check_inputs(input_titles_for_test)

    def check_inputs(self, input_titles_for_test):
        for index, input in enumerate(self.inputs):
            header = input.find_element(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader")
            if header.text != input_titles_for_test[index]:
                print(f"Incorrect title found '{input.text}' required '{input_titles_for_test[index]}'")
                self.inputs_test = False
                return
        self.inputs_test = True
        print("Form check success!")

    def fill_form(self, data, addresses, data_order,input_titles_for_test, time, value):
        if data and addresses:
            for index, entry in enumerate(data[0]["Value"]):
                self.browser.implicitly_wait(10)
                self.find_inputs(input_titles_for_test)
                for indx, input in enumerate(self.inputs):
                    inpt_obj = input.find_element(By.TAG_NAME, "input")
                    inpt_obj.clear()
                    if index + 1 > len(addresses):
                        print("Finish addresses")
                        return 0
                    if data_order[indx] == "Address":
                        entry_data = addresses[index]
                    else:
                        entry_data = data[0][data_order[indx]][index]
                    inpt_obj.send_keys(entry_data)

                self.browser.implicitly_wait(10)
                btn = self.browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
                btn.click()
                print(f"Form {index + 1} completed!")

                self.browser.implicitly_wait(10)
                link = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
                link.click()
            print("Finish data")


        


# For testing
if __name__ == "__main__":
    from python_json_config import ConfigBuilder
    builder = ConfigBuilder()
    config = builder.parse_config("./config.json")

    form = Form(config.webdriver.driver_path, config.webdriver.options, config.form.url)
    form.find_inputs(config.form.input_titles)