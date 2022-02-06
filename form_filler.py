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

    def fill_form(self, data, addresses, data_order, input_titles_for_test, time, values_list):
        minutes = self.convert_time_to_minutes(time)
        form_counter = 1
        print(values_list)
        if data and addresses:
            for index, entry in enumerate(data[0]["Value"]):
                data_minutes = data[0]["Age"][index]
                data_value = data[0]["Value"][index]
                if data_minutes > minutes:
                    print("Finish time")
                    return
                if data_value not in values_list:
                    continue
                self.browser.implicitly_wait(10)
                self.find_inputs(input_titles_for_test)

                for indx, input in enumerate(self.inputs):
                    entry_data = None
                    input_type = data_order[indx].split("-")[0].lower()

                    if input_type != "radio" and input_type != "checkbox" and input_type != "dropdown":
                        inpt_obj = input.find_element(By.TAG_NAME, "input")
                        inpt_obj.clear()
                    

                    if index + 1 > len(addresses):
                        print("Finish addresses")
                        return 0

                    if data_order[indx] == "Address_from_file":
                        entry_data = addresses[form_counter - 1]

                    elif input_type == "radio":
                        choise = int(data_order[indx].split("-")[1])
                        radio_buttons = self.inputs[indx].find_elements(By.CLASS_NAME, "appsMaterialWizToggleRadiogroupElContainer")
                        if radio_buttons:
                            radio_buttons[choise-1].click()

                    elif input_type == "checkbox":
                        choises = data_order[indx].split("-")[1:]
                        checkboxes = self.inputs[indx].find_elements(By.CLASS_NAME, "docssharedWizToggleLabeledContent")
                        for choise in choises:
                            checkboxes[int(choise) - 1].click()
                    
                    #TODO: Neveikia dropdown list
                    # elif input_type == "dropdown":
                    #     choise = data_order[indx].split("-")[1]

                    #     dropdown = self.inputs[indx].find_element(By.CLASS_NAME, "quantumWizMenuPaperselectOption")
                    #     if dropdown:
                    #         dropdown.click()
                    #         options = self.inputs[indx].find_elements(By.CSS_SELECTOR, ".quantumWizMenuPaperselectContent.exportContent")

                    #         if options:
                    #             print(options[1].text)
                        

                    else:
                        entry_data = data[0][data_order[indx]][index]
                    
                    if entry_data:
                        inpt_obj.send_keys(entry_data)

                self.browser.implicitly_wait(10)
                btn = self.browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
                btn.click()
                print(f"Form {form_counter} completed!")
                form_counter += 1

                self.browser.implicitly_wait(10)
                link = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
                link.click()
            print("Finish data")

    def convert_time_to_minutes(self, time):
        time_list = time.split(" ")
        minutes = 0
        if time_list[1].lower() == "min" or time_list[1].lower() == "mins":
            minutes = int(time_list[0])
        elif time_list[1].lower() == "hr" or time_list[1].lower() == "hrs":
            minutes = int(time_list[0]) * 60
            if len(time_list) > 4:
                minutes += int(time_list[2])
        elif time_list[1].lower() == "day" or time_list[1].lower() == "days":
            minutes = int(time_list[0]) * 1440
            if len(time_list) > 4:
                minutes += int(time_list[2]) * 60
        return minutes


# For testing
if __name__ == "__main__":
    from python_json_config import ConfigBuilder
    builder = ConfigBuilder()
    config = builder.parse_config("./config.json")

    form = Form(config.webdriver.driver_path, config.webdriver.options, config.form.url)
    form.find_inputs(config.form.input_titles)