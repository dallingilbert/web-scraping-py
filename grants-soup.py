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

# wait for the dynamic content to load
try:
    # grab our keyword search table
    tables = driver.find_elements(By.TAG_NAME, "table")

    # isolate keyword search input
    keyword_search = tables[1].find_element(By.ID, "keyword")

    # fill keyword with search criteria
    keyword_search.send_keys("technology")

    # check our inputs value
    print(keyword_search.get_attribute("value"))

    # find our search button element and click it
    tables[1].find_element(By.ID, "searchBtn").click()

    # grab info from main table
    search_results = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid")))

    tbody = search_results.find_element(By.TAG_NAME, "tbody")

    # split the tbody into tables of data
    table_even = tbody.find_elements(By.CLASS_NAME, "gridevenrow")
    table_odd = tbody.find_elements(By.CLASS_NAME, "gridoddrow")

    # combine even and odd rows
    data = table_even + table_odd

    # extract the opportunity number
    opp_list = []

    for d in data:
        try:
            opp_link = d.find_element(By.TAG_NAME, "a")
            # navigate to opportunity link webpage
            opp_link.click()
            # select the div with info synopsis
            synopsis_content = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.ID, "synopsisDetailsContent"))
            )

            # seperate content by fieldsets
            fieldset = synopsis_content.find_elements(By.TAG_NAME, "fieldset")

            print(fieldset)

            # table body
            t_body = fieldset[0].find_element(By.TAG_NAME, "tbody")

            # navigate back to the home page
            driver.back()

        except exceptions.StaleElementReferenceException as e:
            print(e)

        # opp_list.append(opportunity_link.text)
finally:
    driver.quit()
