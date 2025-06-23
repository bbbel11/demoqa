import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import time

fake = Faker()


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_practice_form(browser):

    wait = WebDriverWait(browser, 20)


    browser.get("https://demoqa.com/automation-practice-form")


    wait.until(EC.presence_of_element_located((By.ID, "firstName")))


    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    mobile = fake.msisdn()[:10]
    current_address = fake.address().replace("\n", " ")


    browser.find_element(By.ID, "firstName").send_keys(first_name)


    browser.find_element(By.ID, "lastName").send_keys(last_name)


    browser.find_element(By.ID, "userEmail").send_keys(email)


    male_radio = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(text(),'Male')]")))
    male_radio.click()


    browser.find_element(By.ID, "userNumber").send_keys(mobile)


    dob_input = wait.until(EC.element_to_be_clickable((By.ID, "dateOfBirthInput")))
    dob_input.click()


    month_select = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "react-datepicker__month-select")))
    month_select.send_keys("May")


    year_select = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "react-datepicker__year-select")))
    year_select.send_keys("1990")


    day = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "react-datepicker__day--015")))
    day.click()


    subjects_input = wait.until(EC.element_to_be_clickable((By.ID, "subjectsInput")))
    subjects_input.send_keys("Maths")
    subjects_input.send_keys(Keys.ENTER)


    sports_checkbox = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(text(),'Sports')]")))
    sports_checkbox.click()


    browser.find_element(By.ID, "currentAddress").send_keys(current_address)


    state_div = wait.until(EC.element_to_be_clickable((By.ID, "state")))
    browser.execute_script("arguments[0].scrollIntoView(true);", state_div)
    browser.execute_script("arguments[0].click();", state_div)

    ncr_option = wait.until(EC.element_to_be_clickable(
        (By.ID, "react-select-3-option-0")))
    browser.execute_script("arguments[0].click();", ncr_option)


    city_div = wait.until(EC.element_to_be_clickable((By.ID, "city")))
    browser.execute_script("arguments[0].click();", city_div)

    delhi_option = wait.until(EC.element_to_be_clickable(
        (By.ID, "react-select-4-option-0")))
    browser.execute_script("arguments[0].click();", delhi_option)


    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(1)
    browser.execute_script("arguments[0].click();", submit_button)


    modal = wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "modal-content")))
    modal_text = modal.text


    assert f"Student Name {first_name} {last_name}" in modal_text
    assert f"Student Email {email}" in modal_text
    assert "Gender Male" in modal_text
    assert f"Mobile {mobile}" in modal_text
    assert "Date of Birth 15 May,1990" in modal_text
    assert "Subjects Maths" in modal_text
    assert "Hobbies Sports" in modal_text
    assert f"Address {current_address}" in modal_text
    assert "State and City NCR Delhi" in modal_text


    close_button = wait.until(EC.element_to_be_clickable(
        (By.ID, "closeLargeModal")))
    close_button.click()