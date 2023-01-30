from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

from test_data import (
    VALID_PATIENT_IDs,
    INVALID_PATIENT_IDs,
    NON_EXISTING_PATIENT_IDs,
    BASE_URL,
)


@pytest.fixture
def driver():
    _driver = webdriver.Chrome()
    yield _driver
    _driver.close()


@pytest.mark.parametrize("id", VALID_PATIENT_IDs)
def test_search_valid_id(driver, id):
    # navigate to the search page
    driver.get(BASE_URL)

    # locate the search input element
    search_input = driver.find_element(by=By.ID, value="tbx_identifier")

    # enter a search query
    search_input.send_keys(id)

    # locate the search button element
    search_button = driver.find_element(by=By.CLASS_NAME, value="search-btn")

    # click the search button
    search_button.click()

    # wait for the search results page to load
    driver.implicitly_wait(2)

    # assert that the search results page is displayed
    assert "Search Results" in driver.title

    patient_found_msg = driver.find_element(by=By.ID, value="patient_found_msg")
    patient_details = driver.find_element(by=By.ID, value="patient_details")
    details = patient_details.get_attribute("innerHTML")

    # Assert that the patient found message is displayed
    assert patient_found_msg.is_displayed
    assert patient_found_msg.text == "Patient Found"

    # assert that the patient details are displayed
    assert patient_details.is_displayed
    assert details.find("Name")
    assert details.find("DOB")
    assert details.find("Gender")


@pytest.mark.parametrize("id", NON_EXISTING_PATIENT_IDs)
def test_search_non_existing_id(driver, id):
    driver.get(BASE_URL)

    # locate the search input element
    search_input = driver.find_element(by=By.ID, value="tbx_identifier")

    # enter a search query
    search_input.send_keys(id)

    # locate the search button element
    search_button = driver.find_element(by=By.CLASS_NAME, value="search-btn")

    # click the search button
    search_button.click()

    # wait for the search results page to load
    driver.implicitly_wait(2)

    # assert that the search results page is displayed
    assert "Search Results" in driver.title

    patient_not_found_err_msg = driver.find_element(by=By.ID, value="not_found_err")
    patient_not_found_err_msg_txt = patient_not_found_err_msg.get_attribute("innerHTML")
    identifier = driver.find_element(by=By.ID, value="identifer")
    identifier_txt = identifier.get_attribute("innerHTML")

    # assert that the patient not found message is displayed
    assert patient_not_found_err_msg.is_displayed
    assert patient_not_found_err_msg_txt == "No patient matches the identifier"
    assert identifier.is_displayed
    assert identifier_txt in driver.current_url


@pytest.mark.parametrize("id", INVALID_PATIENT_IDs)
def test_search_invalid_ids(driver, id):
    driver.get(BASE_URL)

    # locate the search input element
    search_input = driver.find_element(by=By.ID, value="tbx_identifier")

    # enter a search query
    search_input.send_keys(id)

    # locate the search button element
    search_button = driver.find_element(by=By.CLASS_NAME, value="search-btn")

    # click the search button
    search_button.click()

    # wait for the search results page to load
    driver.implicitly_wait(2)

    # assert that the search results page is displayed
    assert "Search Results" in driver.title

    invalid_patient_id_err_msg = driver.find_element(by=By.ID, value="not_found_err")
    invalid_patient_id_err_msg_txt = invalid_patient_id_err_msg.get_attribute(
        "innerHTML"
    )
    identifier = driver.find_element(by=By.ID, value="identifer")

    # assert that the Invlid message is displayed
    assert invalid_patient_id_err_msg.is_displayed
    assert invalid_patient_id_err_msg_txt == "Invalid patient id"
    assert identifier.is_displayed