from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

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

# function defining how we scrape each grant opportunity


def scrape_grant_opp():
    # select the div with info synopsis
    synopsis_content = WebDriverWait(driver, 60).until(
        EC.visibility_of_all_elements_located(
            (By.ID, "synopsisDetailsContent"))
    )

    # seperate page content by fieldsets
    fieldset = synopsis_content[0].find_elements(By.TAG_NAME, "fieldset")

    # retrieve general body info
    div_content = fieldset[0].find_elements(By.TAG_NAME, "div")
    print(div_content)

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


def loop_links(results):
    tbody = results.find_element(By.TAG_NAME, "tbody")

    # extract the opportunity number
    trow = tbody.find_elements(By.TAG_NAME, "tr")

    # skips the first table row and loops opp_links
    for row in trow[1:]:
        try:
            # navigate to opportunity link webpage
            opp_link = row.find_element(By.TAG_NAME, "a")
            # print(opp_link.text)

            # navigate to opp link
            opp_link.click()

            # scrape page
            scrape_grant_opp()

            # navigate back to the home page
            driver.back()
        except exceptions.StaleElementReferenceException as e:
            print(e)


# wait for the dynamic content to load
try:
    # search technology field
    perform_search("technology")

    # grab info from main table
    search_results = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid")))

    # loop through table for opportunity links
    loop_links(search_results)

finally:
    driver.quit()
