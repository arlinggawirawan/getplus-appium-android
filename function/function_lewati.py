from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from config.conftest import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
import time


def handle_blocked_popup(driver):
    wait = WebDriverWait(driver, 30)
    blocked_popups = {
        "com.getplus.application:id/tv_title": {"text": "Selamat datang di GetPlus!"},
        "com.getplus.application:id/tv_detail": {"text": "Jadilah member, kumpulkan poin dari merchant favoritmu dan "
                                                         "redeem dengan berbagai rewards menarik hanya di GetPlus!"},
        "com.getplus.application:id/btn_primary_cta": {"text": "Register"},
        "com.getplus.application:id/tv_secondary_cta": {"text": "Sudah punya akun ? Login"}
    }
    try:
        for blocked_popup, attributes in blocked_popups.items():
            popup = wait.until(
                expected.visibility_of_element_located((
                    By.ID, blocked_popup)))
            print(f'Pop up with {blocked_popup} is present')

            for attr_names, expected_value in attributes.items():
                actual_value = popup.get_attribute(attr_names)
                assert actual_value == expected_value, (f'Attribute {attr_names} of element {blocked_popup} does not '
                                                        f'match expected value: {expected_value}')
                print(f"Attribute {attr_names} of element {blocked_popup} matches expected value: {expected_value}")
    except NoSuchElementException as e:
        print(f"One or more elements were not found: {e}")


def touch_outside(driver):
    wait = WebDriverWait(driver, 30)
    # Touch outside after pop up blocked appear
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            touch = wait.until(
                expected.presence_of_element_located((
                    By.ID, "com.getplus.application:id/touch_outside")))
            touch.click()
            break
        except StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying...")
            retries += 1


def touch_back(driver):
    wait = WebDriverWait(driver, 10)
    # Touch back function
    navigate_back_elements = wait.until(
        expected.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.ImageButton")))
    # Check if there are multiple back buttons
    if len(navigate_back_elements) >= 2:
        for element in navigate_back_elements:
            element.click()
            time.sleep(3)  # Adjust the delay time as needed based on application's responsiveness
    elif len(navigate_back_elements) == 1:
        navigate_back_elements[0].click()
    else:
        print("No back button found.")


def back(driver):
    wait = WebDriverWait(driver, 30)
    back_button = wait.until(
        expected.element_to_be_clickable((
            AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                            "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                            "android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[1]/"
                            "android.widget.ImageButton"
        )))
    back_button.click()


def scroll(driver):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(544, 2035)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(540, 1038)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def scroll_homepage(driver):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(327, 1966)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(350, 395)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
