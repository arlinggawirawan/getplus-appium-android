from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from function.function_lewati import handle_blocked_popup, touch_outside
from config.conftest import driver


class GuestAndroidUiAutomator:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def handle_convert(self, element_text):
        element = self.wait.until(
            expected.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().className("android.widget.TextView").text("{element_text}")'
            ))
        )
        element.click()
        handle_blocked_popup(self.driver)
        touch_outside(self.driver)
