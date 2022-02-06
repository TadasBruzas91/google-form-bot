from web_scraper import Scraper
from form_filler import Form
from python_json_config import ConfigBuilder


def get_addresses():
    addresses = []
    with open("addresses.txt", encoding="utf-8") as f:
        for line in f:
            addresses.append(line.rstrip())
    return addresses


builder = ConfigBuilder()
config = builder.parse_config("./config.json")

addresses_from_file = get_addresses()

scraper = Scraper(config.webdriver.driver_path, config.webdriver.options, config.scraper.base_url)
scraper.go_to_address(config.scraper.address)
scraper.got_to_out_transactions()
scraper.save_table_data()
scraped_data = scraper.get_scraped_data()
scraper.close()

form = Form(config.webdriver.driver_path, config.webdriver.options, config.form.url)
form.fill_form(scraped_data, addresses_from_file, config.form.data_order, config.form.input_titles, config.transaction_setup.age, config.transaction_setup.value)
form.close()