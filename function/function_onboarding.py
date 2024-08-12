import time
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from config.conftest import driver_onboarding
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected


class OnboardingHelper:
    HEADER_TEXT_1 = "Raih rewards dari transaksi sehari-hari"
    HEADER_TEXT_2 = "Dapatkan poin dengan transaksi di banyak merchant"
    HEADER_TEXT_3 = "Bisa dapat poin dari belanja offline maupun online"

    BODY_TEXT_1 = "Kumpulkan poin dari tiap transaksi dan tukarkan jadi berbagai rewards menarik"
    BODY_TEXT_2 = "Upload struk dari merchant partner GetPlus untuk kumpulkan ribuan poinnya"
    BODY_TEXT_3 = "Termasuk belanja online di ecommerce kesayangan juga dapat poin loh"

    def __init__(self, driver_onboarding):
        self.driver = driver_onboarding
        self.wait = WebDriverWait(self.driver, 30)

    def button_onboarding_popup(self):
        onboarding_popups = {
            "com.getplus.application:id/btn_login": {"text": "Masuk"},
            "com.getplus.application:id/btn_join": {"text": "Daftar"},
            "com.getplus.application:id/tv_masuk_sebagi_tamu": {"text": "Masuk Sebagai Tamu →"}
        }

        try:
            for onboarding_popup, attributes in onboarding_popups.items():
                popup = self.wait.until(
                    expected.visibility_of_element_located((
                        By.ID, onboarding_popup))
                )
                print(f'Pop up with {onboarding_popup} is present')

                for attr_names, expected_value in attributes.items():
                    actual_value = popup.get_attribute(attr_names)
                    assert actual_value == expected_value, (f'Attribute {attr_names} of element {onboarding_popup} '
                                                            f'does not match expected value: {expected_value}')
                    print(f"Attribute {attr_names} of element {onboarding_popup} "
                          f"matches expected value: {expected_value}")

        except NoSuchElementException as e:
            print(f"One or more elements were not found: {e}")

    def touch_hold(self):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        touch_duration = 5
        start_time = time.time()
        while time.time() - start_time < touch_duration:
            actions.w3c_actions.pointer_action.move_to_location(563, 646)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.perform()

            time.sleep(0.5)
