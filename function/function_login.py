import pytest
from config.conftest import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected


@pytest.mark.usefixtures("driver")
class HandleErrorLogin:

    @staticmethod
    def check_popup_error(driver):
        wait = WebDriverWait(driver, 30)
        popup_error = wait.until(
            expected.presence_of_element_located((
                By.ID, "com.getplus.application:id/tv_detail")))
        assert popup_error.get_attribute('text') == "data not found", "Validation error"

    @staticmethod
    def check_popup_error_click(driver):
        wait = WebDriverWait(driver, 30)
        popup_error_click = wait.until(
            expected.element_to_be_clickable((
                By.ID, "com.getplus.application:id/btn_positive")))
        popup_error_click.click()
