import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from config.conftest import driver
from function.marketing_layouts import HandleAirshipElement
from function.function_login import HandleErrorLogin
from function.function_onboarding import OnboardingHelper
from function.handler.format_handler import FormatHandler
from function.handler.credentials import Credentials


@allure.epic("Test Case Login")
@allure.story("As a registered user, I want to login GetPlus App")
@allure.tag("Android", "Regression test")
@allure.label("owner", "Arlingga")
class TestLogin:
    email_formats = FormatHandler.get_email_formats()
    phone_numbers = FormatHandler.get_phone_numbers()
    walkthrough_texts = FormatHandler.get_walkthrough_text()
    credentials = Credentials.get_credential()
    username = credentials["username"]
    password = credentials["password"]
    phone_no = credentials["phoneNo"]

    @allure.description("This test to validate login page design")
    @allure.title("Verify login page design")
    def test_login_page(self, driver):
        wait = WebDriverWait(driver, 30)
        try:
            with allure.step("Check lewati button"):
                # Verify UI design, button and Text
                lewati_button = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/tv_skip"))
                )
                assert lewati_button.text == 'Lewati', "Element text does not match"
                print(f'{lewati_button.text} button is visible')

            with allure.step("Check forgot password button"):
                forgot_password = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/tv_forget"))
                )
                assert forgot_password.text == 'Lupa kata sandi?', "Element text does not match"
                print(f'{forgot_password.text} button is visible')

            with allure.step("Check signup button"):
                signup_button = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/tv_signup"))
                )
                assert signup_button.text == 'Daftar Sekarang', "Element text does not match"
                print(f'{signup_button.text} button is visible')

            with allure.step("Check masking/unmasking password button"):
                masking_password = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/text_input_end_icon"))
                )
                masking_password.click()
                assert masking_password.get_attribute('checked') == 'true', "Element is not checked"
                print("Masking password button is working")

            with allure.step("Check placeholder in input box"):
                # Verify placeholder text in input box username & password
                placeholder_username = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/et_username"))
                )
                placeholder_password = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/et_password"))
                )
                placeholders = [placeholder_username, placeholder_password]
                expected_placeholders = ["Masukkan Email / Nomor HP", "Masukkan Kata Sandi"]
                for placeholder, expected_text in zip(placeholders, expected_placeholders):
                    # Get the placeholder text of the element
                    actual_text = placeholder.text
                    print(f"Actual text: {actual_text}, Expected text: {expected_text}")
                    # Assert the placeholder text
                    assert actual_text == expected_text, \
                        f"Actual placeholder '{actual_text}' does not match expected placeholder '{expected_text}'"
                    print("Placeholder is correct")

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Verify login with valid email")
    @allure.description("This test to validate login for existing and registered user")
    def test_valid_login(self, driver, login_flow=True, assertion_flow=True, greetings=True):
        wait = WebDriverWait(driver, 30)
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver)
        try:
            if login_flow:
                with allure.step("Input valid email"):
                    # Input valid username
                    username_field = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/et_username"))
                    )
                    username_field.click()
                    username_field.send_keys(self.username)

                with allure.step("Input password"):
                    # Input valid password
                    password_field = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/et_password"))
                    )
                    password_field.click()
                    password_field.send_keys(self.password)

                with allure.step("Click on masuk button"):
                    # Click on login button
                    login_button = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/bt_login"))
                    )
                    login_button.click()

                time.sleep(5)

            if assertion_flow:
                with allure.step("Verify login successfull, assert that notif permission appear"):
                    # Assertion of asking user permission and do action
                    notif_permission = wait.until(
                        expected.presence_of_element_located((
                            By.ID, "com.android.permissioncontroller:id/permission_message"))
                    )
                    assert notif_permission.text == 'Allow GetPlus to send you notifications?', ("Element text does "
                                                                                                 "not match")
                    print(f'Notification permission title: {notif_permission.text} is visible')

                    notif_permission_click = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.android.permissioncontroller:id/permission_allow_button"))
                    )
                    notif_permission_click.click()

                with allure.step("Verify popup promo appear"):
                    popup_promo = wait.until(
                        expected.presence_of_element_located((
                            By.ID, "com.getplus.application:id/tv_title"))
                    )
                    assert popup_promo.text == 'Dapatkan promo menarik\ndisekitar Kamu!', "Element text does not match"
                    print(f'Pop Up promo title: {popup_promo.text} is visible')

                    popup_promo_click = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/btn_positive"))
                    )
                    popup_promo_click.click()

                with allure.step("Verify walkthrough is appear"):
                    for index, text in enumerate(self.walkthrough_texts):
                        walkthrough_page = wait.until(
                            expected.visibility_of_element_located((
                                By.ID, "com.getplus.application:id/tv_title"))
                        )
                        assert walkthrough_page.text == text, f"Element text does not match for page {index + 1}"
                        print(f"Walkthrough page {index + 1} is visible")

                    # Click next button except for the last page
                        if index < len(self.walkthrough_texts) - 1:
                            walkthrough_next = wait.until(
                                expected.element_to_be_clickable((
                                    By.ID, "com.getplus.application:id/btn_next"))
                            )
                            walkthrough_next.click()

                    # Cancel the walkthrough
                    walkthrough_cancel_click = wait.until(
                        expected.element_to_be_clickable((By.ID, "com.getplus.application:id/img_cancel"))
                    )
                    walkthrough_cancel_click.click()

                with allure.step("Verify location permission is appear"):
                    location_permission = wait.until(
                        expected.visibility_of_element_located((
                            By.ID, "com.android.permissioncontroller:id/permission_message"))
                    )
                    assert location_permission.text == 'Allow GetPlus to access this device’s location?', \
                        "Element text does not match"
                    print(f'Location permission title: {location_permission.text} is visible')

                    location_permission_click = wait.until(
                        expected.visibility_of_element_located((
                            By.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"))
                    )
                    location_permission_click.click()

            if greetings:
                with allure.step("Assert login flow success, verify greetings user name appear"):
                    login_success = wait.until(
                        expected.visibility_of_element_located((
                            By.ID, "com.getplus.application:id/tv_user_name"))
                    )
                    assert login_success.text == 'Hi Gpites01 :)', "Success login but catch error"
                    print(f'Login success: {login_success.text}, account greeting is appear')

                time.sleep(3)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Verify login with valid phone number")
    @allure.description("This test to validate login for existing and registered user")
    def test_valid_phonenumber(self, driver):
        wait = WebDriverWait(driver, 30)
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver)
        try:
            with allure.step("Input valid phone number"):
                # Input valid username
                username_field = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_username"))
                )
                username_field.click()
                username_field.send_keys(self.phone_no)

            with allure.step("Input password"):
                # Input valid password
                password_field = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_password"))
                )
                password_field.click()
                password_field.send_keys(self.password)

            with allure.step("Click on masuk button"):
                # Click on login button
                login_button = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/bt_login"))
                )
                login_button.click()

            with allure.step("Assert login success, check notif permission appear"):
                # Assertion of login success with expect notification permission is apper
                notif_permission = wait.until(
                    expected.presence_of_element_located((
                        By.ID, "com.android.permissioncontroller:id/permission_message"))
                )
                assert notif_permission.text == 'Allow GetPlus to send you notifications?', ("Element text "
                                                                                             "does not match")
                print(f'Notification title: {notif_permission.text} is visible, login with phone number success')

            time.sleep(5)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Verify validation login page with invalid credentials and format validation")
    @allure.description("This test to validate login page with invalid credentials and format validation should "
                        "not be able to login")
    def test_invalid_login(self, driver):
        onboarding_helper = OnboardingHelper(driver)
        time.sleep(6)
        onboarding_helper.touch_hold()
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver)
        wait = WebDriverWait(driver, 30)
        try:
            with allure.step("Check input format phone number"):
                for phone_number in self.phone_numbers:
                    phone_field = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/et_username"))
                    )
                    phone_field.click()
                    phone_field.clear()
                    phone_field.send_keys(phone_number)

                    if len(phone_number) < 10:
                        error_message = wait.until(
                            expected.visibility_of_element_located((
                                By.ID, "com.getplus.application:id/tv_emailid_empty"))
                        )
                        assert error_message.text == "Format nomor handphone tidak sesuai", "Element does not exist"
                        print(f"Validation passed for {phone_number}: Error message displayed as expected")

                    else:
                        error_message = wait.until(
                            expected.invisibility_of_element_located((
                                By.ID, "com.getplus.application:id/tv_emailid_empty"))
                        )
                        assert error_message, "Error message still appear"
                        print(f"Validation passed for {phone_number}: No error message displayed")

            with allure.step("Check input format email"):
                for email_format in self.email_formats:
                    email_field = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/et_username"))
                    )
                    email_field.click()
                    email_field.clear()
                    email_field.send_keys(email_format)

                    email_validation = wait.until(
                        expected.visibility_of_element_located((
                            By.ID, "com.getplus.application:id/tv_emailid_empty"))
                    )
                    assert email_validation.text == 'Format email tidak sesuai', "Element does not exist"
                    print("Email format validation is correct")

            time.sleep(3)

            with allure.step("Check if format not match, masuk button should disable"):
                # Validate Login button should not enabled when password input less than 8 character
                email_fields = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_username"))
                )
                email_fields.clear()
                email_fields.send_keys(self.username)
                password_field = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_password"))
                )
                password_field.click()
                password_field.send_keys("xxxxxxx")

                validation_loginbutton = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/bt_login"))
                )
                assert validation_loginbutton.get_attribute("enabled") == 'false', "Button should be disabled"
                print("Login button is disabled when password less than 8 character")

                # Validate Login button should not enabled when email in wrong format but password is valid
                email_fields.clear()
                email_fields.send_keys("gpites01+qagmail.com")
                password_field.click()
                password_field.send_keys(self.password)
                assert validation_loginbutton.get_attribute("enabled") == 'false', "Button should be disabled"
                print("Login button is disabled when email in wrong format but password is valid")

            time.sleep(3)

            with allure.step("Check login with invalid password should not able to login"):
                # Validate login with invalid password
                email_fields = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_username"))
                )
                email_fields.click()
                email_fields.send_keys("gpites01+qa@gmail.com")
                password_field.click()
                password_field.send_keys("xxxxxxx")
                login_button = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/bt_login"))
                )
                login_button.click()

            with allure.step("Check toast error message"):
                toast_error = wait.until(
                    expected.presence_of_element_located((
                        By.XPATH, "/hierarchy/android.widget.Toast"))
                )
                assert toast_error.get_attribute('text') == "Email atau kata sandi salah", "Validation Error"
                print(f"Validation success, can't login with invalid password")

            with allure.step("Check login with invalid email should not able to login"):
                # Validate login with invalid username
                email_fields = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_username"))
                )
                email_fields.click()
                email_fields.send_keys("gpites01+qa123@gmail.com")
                password_field.click()
                password_field.send_keys("Gxxxxxxxx")
                login_button.click()

            with allure.step("Check Pop up error message"):
                HandleErrorLogin.check_popup_error(driver)
                HandleErrorLogin.check_popup_error_click(driver)

            with allure.step("Check login with invalid phone number should not able to login"):
                # Validate login with invalid phone number
                email_fields = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_username"))
                )
                email_fields.click()
                email_fields.send_keys("088294185898")
                password_field.click()
                password_field.send_keys("xxxxxxx")
                login_button.click()

            with allure.step("Check toast error message"):
                HandleErrorLogin.check_popup_error(driver)
                HandleErrorLogin.check_popup_error_click(driver)

            time.sleep(5)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))

    @allure.title("Verify reset password page")
    @allure.description("This test to validate reset password page for existing and registered user")
    def test_forgot_password(self, driver):
        onboarding_helper = OnboardingHelper(driver)
        time.sleep(6)
        onboarding_helper.touch_hold()
        handle_random_element = HandleAirshipElement()
        handle_random_element.start(driver)
        wait = WebDriverWait(driver, 30)
        try:
            with allure.step("Check reset password button should redirect to reset password page"):
                # Verify forgot password button should redirect to forgot password page and default button disabled
                forgot_password = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/tv_forget"))
                )
                forgot_password.click()

                forgot_page = wait.until(
                    expected.presence_of_element_located((
                        By.ID, "com.getplus.application:id/tv_title_forgot_password"))
                )
                assert forgot_page.text == 'Lupa Kata Sandi', "Element text does not appear"
                print("Redirecting to forgot page success")

            with allure.step("Check default reset button should disabled"):
                forgot_button = wait.until(
                    expected.presence_of_element_located((
                        By.ID, "com.getplus.application:id/bt_reset"))
                )
                assert forgot_button.get_attribute('enabled') == 'false', "Button is not disabled"
                print("Button disabled by default")

            with allure.step("Check placeholder"):
                # Verify placeholder text and validation format email
                forgot_placeholder = wait.until(
                    expected.presence_of_element_located((
                        By.ID, "com.getplus.application:id/et_email_address"))
                )
                assert forgot_placeholder.get_attribute('text') == "Masukkan email", "Element text does not match"

            with allure.step("Verify email format in reset password page"):
                for email_format in self.email_formats:
                    email_field = wait.until(
                        expected.element_to_be_clickable((
                            By.ID, "com.getplus.application:id/et_email_address"))
                    )
                    email_field.click()
                    email_field.clear()
                    email_field.send_keys(email_format)

                    email_validation = wait.until(
                        expected.visibility_of_element_located((
                            By.ID, "com.getplus.application:id/tv_email_validation"))
                    )
                    assert email_validation.text == 'Format email tidak sesuai', "Element does not exist"
                    print("Email format validation is correct")

            with allure.step("Verify not registered email should shown error popup"):
                # Verify email is not registered should shown pop up error
                forgot_mail = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_email_address"))
                )
                forgot_mail.clear()
                forgot_mail.click()
                forgot_mail.send_keys("gpites01+123qa123@gmail.com")
                forgot_button.click()

                forgot_error = wait.until(
                    expected.presence_of_element_located((
                        By.XPATH, "/hierarchy/android.widget.Toast"))
                )
                assert forgot_error.get_attribute('text') == 'Email tidak terdaftar atau belum selesai didaftarkan.', \
                    "Validation error"
                print("Validation email is not registered success")

            with allure.step("Verify success sent forgot password to email"):
                # Verify successfull forgot password
                forgot_mail = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/et_email_address"))
                )
                forgot_mail.click()
                forgot_mail.send_keys("gpites01+qa@gmail.com")
                forgot_button.click()

                popup_success = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/tv_title"))
                )
                assert popup_success.text == 'Email telah terkirim!', "Send to email forgot password error"
                print(f'{popup_success.text}, success send forgot password to email')

            with allure.step("After click on OK button, back to login page"):
                # Verify click OK should go back to Login page
                popup_button = wait.until(
                    expected.element_to_be_clickable((
                        By.ID, "com.getplus.application:id/btn_positive"))
                )
                popup_button.click()

                selamat_datang = wait.until(
                    expected.visibility_of_element_located((
                        By.ID, "com.getplus.application:id/tv_login_text"))
                )
                assert selamat_datang.text == 'Selamat datang', "Error, does not back to login page"
                print(f'{selamat_datang.text} is appear, success back to login page')

            time.sleep(5)

        except Exception as e:
            # Handle the failed assertion
            allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Assertion failed: {}".format(str(e)))
