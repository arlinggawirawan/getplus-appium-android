from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from config.conftest import driver
import pytest
import allure
import time

@pytest.fixture(scope="function")
def login(driver):
    from test.GetPlus_login_rebuild import test_valid_login
    test_valid_login(driver, login_flow=True, assertion_flow=True, greetings=True)
    time.sleep(3)


@allure.epic("Test Case Merchant Page")
@allure.story("After Login GetPlus, I want to check list of merchant that cooperation with Getplus")
@allure.description("This test check landing page are met the requirement")
@allure.tag("Android", "5.1.0",)
@allure.label("owner", "Arlingga")
@allure.title("Test merchant landing page")
def test_merchant_page(driver):
    wait = WebDriverWait(driver, 30)
    with allure.step("Open merchant page"):
        merchant = wait.until(expected.element_to_be_clickable((
            By.ID, 'com.getplus.application:id/nav_item_merchant')))
        merchant.click()
        merchant_terbaru = wait.until(
            expected.presence_of_element_located((
                By.ID, 'com.getplus.application:id/tv_merchant_home_heading')))
        try:
            assert merchant_terbaru.get_attribute("text") == 'Merchant terbaru', 'Element does not match'
        except AssertionError:
            allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
            raise