import pandas as pd
import time
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from business import Business


class Scraper:
    def __init__(self):
        self.url = "https://www.rexburg.org/business_directory"
        self.page_num = 0
        self.driver_path = "path/to/chromedriver"

    def run(self):
        business_data = []
        for x in range(14):
            self.navigate_to_website()
            data = self.extract_business_information()
            # print("Our extracted data:", data)
            for d in data:
                business_data.append(d.to_dict())

            # print(business_data)
            print("Scraped page:", x)

        self.export_to_excel(business_data)

    def navigate_to_website(self):
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode
        service = Service(self.driver_path)
        self.get_dynamic_url()  # grab our dynamic url
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.url)

    def get_dynamic_url(self):
        if (self.page_num != 0):
            self.url = "https://www.rexburg.org/business_directory?page=" + \
                str(self.page_num)
        self.page_num += 1  # increment page number

    def extract_business_information(self):
        business_data = []
        try:
            # grab the table with desired information
            table = self.driver.find_element(
                By.CSS_SELECTOR, "table.views-table")
        except:
            print("Error: Could not access table element in DOM")

        table_rows = table.find_elements(By.TAG_NAME, "tr")

        # loop through results table
        for row in table_rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            name = cells[0].text
            number = cells[1].text
            description = cells[2].text
            website = cells[3].text

            business = Business(name, number, description, website)
            business_data.append(business)

        return business_data

    def export_to_excel(self, business_data):
        df = pd.DataFrame(business_data)
        workbook = Workbook()
        sheet = workbook.active

        for row in dataframe_to_rows(df, index=False, header=True):
            sheet.append(row)

        workbook.save("business_data.xlsx")
        self.driver.quit()
