import allure
import time
from selenium.common.exceptions import TimeoutException
from config.conftest import driver_onboarding
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from function.marketing_layouts import HandleAirshipElement
from function.function_onboarding import OnboardingHelper


@allure.epic("Test Case Onboarding")
@allure.story("After installed GetPlus, There are onboarding page for quick introduction about GetPlus")
@allure.description("This test check various aspects onboarding page are met the requirement")
@allure.tag("Android", "Regression test", )
@allure.label("owner", "Arlingga")
class TestOnboarding:

    @allure.title("Test onboarding page 1")
    def test_onboarding_page1(self, driver_onboarding):
        onboarding_helper = OnboardingHelper(driver_onboarding)
        wait = WebDriverWait(driver_onboarding, 30)
        try:
            with allure.step("Check wording popup in onboarding page 1"):
                onboarding_helper.touch_hold()
                page1_header = wait.until(expected.visibility_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.TextView")'
                                                  f'.text("{OnboardingHelper.HEADER_TEXT_1}")')))
                page1_wording_header = page1_header.get_attribute("text")
                assert page1_wording_header == OnboardingHelper.HEADER_TEXT_1
                print(f'expected: "{OnboardingHelper.HEADER_TEXT_1}", actual: "{page1_wording_header}"')
                page1_body = wait.until(expected.visibility_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.TextView")'
                                                  f'.text("{OnboardingHelper.BODY_TEXT_1}")')))
                page1_wording_body = page1_body.get_attribute("text")
                assert page1_wording_body == OnboardingHelper.BODY_TEXT_1
                print(f'expected: "{OnboardingHelper.BODY_TEXT_1}", actual: "{page1_wording_body}"')

            with allure.step("Check button in popup"):
                onboarding_helper.button_onboarding_popup()

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver_onboarding.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Test onboarding page 2")
    def test_onboarding_page2(self, driver_onboarding):
        onboarding_helper = OnboardingHelper(driver_onboarding)
        time.sleep(7)
        onboarding_helper.touch_hold()
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver_onboarding)
        wait = WebDriverWait(driver_onboarding, 30)
        try:
            with allure.step("Check wording popup in onboarding page 2"):
                onboarding_helper.touch_hold()
                page2_header = wait.until(expected.visibility_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.TextView")'
                                                  f'.text("{OnboardingHelper.HEADER_TEXT_2}")')))
                page2_wording_header = page2_header.get_attribute("text")
                assert page2_wording_header == OnboardingHelper.HEADER_TEXT_2
                print(f'expected: "{OnboardingHelper.HEADER_TEXT_2}", actual: "{page2_wording_header}"')
                page2_body = wait.until(expected.visibility_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.TextView")'
                                                  f'.text("{OnboardingHelper.BODY_TEXT_2}")')))
                page2_wording_body = page2_body.get_attribute("text")
                assert page2_wording_body == OnboardingHelper.BODY_TEXT_2
                print(f'expected: "{OnboardingHelper.BODY_TEXT_2}", actual: "{page2_wording_body}"')

            with allure.step("Check button in popup"):
                onboarding_helper.button_onboarding_popup()

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver_onboarding.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Test onboarding page 3")
    def test_onboarding_page3(self, driver_onboarding):
        onboarding_helper = OnboardingHelper(driver_onboarding)
        try:
            while True:
                time.sleep(6)
                onboarding_helper.touch_hold()
                handle_random_element = HandleAirshipElement()
                handle_random_element.start(driver_onboarding)
                break
        except TimeoutException:
            print("Marketing onboarding did not appear. Continuing with the rest of the test.")
        wait = WebDriverWait(driver_onboarding, 30)
        try:
            with allure.step("Check wording popup in onboarding page 3"):
                time.sleep(7)
                onboarding_helper.touch_hold()
                page3_header = wait.until(expected.visibility_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.TextView")'
                                                  f'.text("{OnboardingHelper.HEADER_TEXT_3}")')))
                page3_wording_header = page3_header.get_attribute("text")
                assert page3_wording_header == OnboardingHelper.HEADER_TEXT_3
                print(f'expected: "{OnboardingHelper.HEADER_TEXT_3}", actual: "{page3_wording_header}"')
                page3_body = wait.until(expected.visibility_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.TextView")'
                                                  f'.text("{OnboardingHelper.BODY_TEXT_3}")')))
                page3_wording_body = page3_body.get_attribute("text")
                assert page3_wording_body == OnboardingHelper.BODY_TEXT_3
                print(f'expected: "{OnboardingHelper.BODY_TEXT_3}", actual: "{page3_wording_body}"')

            with allure.step("Check button in popup"):
                onboarding_helper.button_onboarding_popup()

            time.sleep(3)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver_onboarding.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Test login from onboarding page")
    def test_login_onboarding(self, driver_onboarding):
        onboarding_helper = OnboardingHelper(driver_onboarding)
        time.sleep(6)
        onboarding_helper.touch_hold()
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver_onboarding)
        wait = WebDriverWait(driver_onboarding, 30)
        try:
            with allure.step("Click on masuk button"):
                onboarding_helper.touch_hold()
                login = wait.until(
                    expected.element_to_be_clickable((By.ID, 'com.getplus.application:id/btn_login'))
                )
                login.click()
            with allure.step("Verify login"):
                from test.GetPlus_login_rebuild import TestLogin
                test_onboarding_login = TestLogin()
                test_onboarding_login.test_valid_login(driver_onboarding)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver_onboarding.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Test login as a guest from onboarding page")
    def test_guest_from_onboarding(self, driver_onboarding):
        onboarding_helper = OnboardingHelper(driver_onboarding)
        time.sleep(6)
        onboarding_helper.touch_hold()
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver_onboarding)
        wait = WebDriverWait(driver_onboarding, 30)
        try:
            with allure.step("Click on Masuk Sebagai Tamu ->"):
                onboarding_helper.touch_hold()
                guest_login = wait.until(expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/tv_masuk_sebagi_tamu'))
                )
                guest_login.click()
                from test.GetPlus_lewati_rebuild import test_guest_login
                test_guest_login(driver_onboarding, click_lewati_button=False)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver_onboarding.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))
