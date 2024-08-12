import threading
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from config.conftest import driver
from selenium.webdriver.support import expected_conditions as expected


@pytest.mark.usefixtures("driver")
class HandleAirshipElement:
    @staticmethod
    def check_and_click_airship_layout(driver):
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(
                expected.visibility_of_element_located((
                    By.CLASS_NAME, "com.urbanairship.android.layout.widget.WeightlessLinearLayout"))
            )
            image_button = wait.until(
                expected.element_to_be_clickable((
                        By.CLASS_NAME, "android.widget.ImageButton"))
            )
            image_button.click()
            print("Marketing onboarding appeared was closed")
        except TimeoutException:
            print("Marketing onboarding did not appear. Continuing with the rest of the test.")

    @staticmethod
    def close_airship_reward(driver):
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(
                expected.visibility_of_element_located((
                    AppiumBy.ACCESSIBILITY_ID, "Lihat Rewards"))
            )
            close_airship_reward_button = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.CLASS_NAME, "android.widget.ImageButton"))
            )
            close_airship_reward_button.click()
            print("Marketing reward appeared was closed")
        except TimeoutException:
            print("Marketing reward did not appear. Continuing with the rest of the test.")

    def start(self, driver):
        thread = threading.Thread(target=self.check_and_click_airship_layout, args=(driver,))
        thread.start()

    def start_reward(self, driver):
        thread_rewards = threading.Thread(target=self.close_airship_reward, args=(driver,))
        thread_rewards.start()
