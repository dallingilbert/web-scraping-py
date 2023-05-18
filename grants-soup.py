from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import pandas as pd

import time

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))

# specify the URL of the website to scrape
url = 'https://www.grants.gov/custom/search.jsp'

# load the website in the browser
driver.get(url)

# maximize browser window
driver.maximize_window()

# function to handle exporting our scraped data to an excel file


def export_to_excel(data):
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data)

    # Define the path and filename for the Excel file
    filename = "scraped_data.xlsx"

    # Export the DataFrame to Excel
    df.to_excel(filename, index=False)

# function defining how we scrape each grant opportunity


def scrape_grant_opp(list):
    # select the div with info synopsis
    synopsis_content = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located(
            (By.ID, "synopsisDetailsContent"))
    )

    # seperate page content by fieldsets
    g_fieldset = synopsis_content[0].find_elements(By.TAG_NAME, "fieldset")

    # table row general
    tr_general = g_fieldset[0].find_element(By.TAG_NAME, "tr")

    # Our table data within the table row
    td_general = tr_general.find_elements(By.TAG_NAME, "td")

    # print(td_gen[0].get_attribute("valign"))

    # create opportunity dictionary
    opportunity_dict = {}

    for td in td_general:
        # driver.implicitly_wait(5)
        table_rows = td.find_elements(By.TAG_NAME, "tr")

        # loop through our table row elements for table data
        for tr in table_rows:
            th = tr.find_element(By.TAG_NAME, "th")
            span = tr.find_element(By.TAG_NAME, "span")
            opportunity_dict[th.text] = span.text

     # Append the opportunity dictionary to the tspan_list
    list.append(opportunity_dict)

# function for using our search button


def perform_search(criteria):
    # grab our keyword search table

    tables = driver.find_elements(By.TAG_NAME, "table")

    # isolate keyword search input
    keyword_search = tables[1].find_element(By.ID, "keyword")

    # fill keyword with search criteria
    keyword_search.send_keys(criteria)

    # check our inputs value
    print(keyword_search.get_attribute("value"))

    # find our search button element and click it
    tables[1].find_element(By.ID, "searchBtn").click()

# function for looping through opportunity links


def loop_links(results, list):
    tbody = results.find_element(By.TAG_NAME, "tbody")

    # extract the opportunity number
    trow = tbody.find_elements(By.TAG_NAME, "tr")

    # skips the first table row and loops opp_links
    for row in trow[1:]:
        try:
            # navigate to opportunity link webpage
            opp_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(row.find_element(By.TAG_NAME, "a")))

        except exceptions.StaleElementReferenceException as e:
            print(e)

        # click opportunity link
        opp_link.click()

        # scrape page
        scrape_grant_opp(list)

        # navigate back to the home page
        driver.back()

        # time.sleep(1)


# wait for the dynamic content to load
try:
    # search technology field
    perform_search("technology")

    # grab info from main table
    search_results = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid")))

    # create opportunity list
    tspan_list = []

    # loop through table for opportunity links
    loop_links(search_results, tspan_list)

    # Call the export_to_excel function to export the scraped data
    export_to_excel(tspan_list)


finally:
    driver.quit()
