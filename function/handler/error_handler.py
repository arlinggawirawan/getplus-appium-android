import allure
from config.conftest import driver


def handle_error(driver):
    try:
        pass
    except Exception as e:
        # Handle the failed assertion
        allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
        raise AssertionError("Assertion failed: {}".format(str(e)))
