import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from config.conftest import driver
from function.function_onboarding import OnboardingHelper
from function.marketing_layouts import HandleAirshipElement
from function.function_lewati import handle_blocked_popup, touch_back, touch_outside, back, scroll, scroll_homepage
from test.element.xpath import GuestXpath
from test.element.android_automator import GuestAndroidUiAutomator


@allure.epic("Test Case Login as Guest")
@allure.story("As a new user, I want to login without create account first to explore app")
@allure.description("This test to validate login for guest account by click on lewati button")
@allure.tag("Android", "5.1.0",)
@allure.label("owner", "Arlingga")
@allure.title("Validate login as a guest")
def test_guest_login(driver, click_lewati_button=True):
    wait = WebDriverWait(driver, 30)
    try:
        with allure.step("Click on lewati button"):
            # Verify Login as a guest
            if click_lewati_button:
                lewati_button = wait.until(
                    expected.element_to_be_clickable((By.ID, "com.getplus.application:id/tv_skip")))
                lewati_button.click()

        with allure.step("Validate permission and walkthrough as guest login"):
            from test.GetPlus_login_rebuild import TestLogin
            test_onboarding_login = TestLogin()
            test_onboarding_login.test_valid_login(driver, login_flow=False, greetings=False)

            # Assert login as guest success without interruption
            login_success = wait.until(
                expected.visibility_of_element_located((
                    By.ID, "com.getplus.application:id/tv_user_name")))
            assert login_success.text == 'Halo!', "Element does not match"
            print(f'Login success: {login_success.text}, guest account greeting is appear')

            poin_kamu = wait.until(
                expected.visibility_of_element_located((
                    By.ID, "com.getplus.application:id/tv_home_card_value")))
            assert poin_kamu.text == '0 poin', "Guest account has been compromised"
            print(f'Guest poin visibility = {poin_kamu.text}')

        time.sleep(3)

    except Exception as e:
        # Handle the failed assertion
        allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
        raise AssertionError("Assertion failed: {}".format(str(e)))


@allure.epic("Test Case Login as Guest")
@allure.story("For the security, guest account should block all entry point for the transactional feature")
@allure.description("This test to validate blocked popup for guest account should be visible")
@allure.tag("Android", "5.1.0",)
@allure.label("owner", "Arlingga")
@allure.title("Validate blocked pop up guest in app features")
def test_blocked_popup(driver):
    onboarding_helper = OnboardingHelper(driver)
    wait = WebDriverWait(driver, 30)
    try:
        # List of blocked popup goes here :

        # Scan receipt page blocked popup
        test_guest_login(driver, click_lewati_button=True)
        with allure.step("Validate blocked popup in Struk feature"):
            struk_index = 0
            struk = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, "//*[@resource-id='com.getplus.application:id/ll_card_icon'][position()={}]"
                    .format(struk_index + 1)
                ))
            )
            struk.click()
            time.sleep(2)

            # Blocked popup banner view
            guest_xpath = GuestXpath(driver)
            guest_xpath.banner_scan_receipt_index(1)
            handle_blocked_popup(driver)
            touch_outside(driver)
            guest_xpath.banner_scan_receipt_index(2)
            handle_blocked_popup(driver)
            touch_outside(driver)

            tips_trick = wait.until(
                expected.presence_of_element_located((
                    By.ID, "com.getplus.application:id/tv_tips_and_trick"))
            )
            tips_trick.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            lihat_semua = wait.until(
                expected.presence_of_element_located((
                    By.ID, "com.getplus.application:id/tv_see_all"))
            )
            lihat_semua.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            # Sampling click merchant scan receipt
            guest_xpath.merchant_scan_receipt_index(1)
            handle_blocked_popup(driver)
            touch_outside(driver)
            guest_xpath.merchant_scan_receipt_index(2)
            handle_blocked_popup(driver)
            touch_outside(driver)
            guest_xpath.merchant_scan_receipt_index(7)
            handle_blocked_popup(driver)
            touch_outside(driver)
            guest_xpath.merchant_scan_receipt_index(6)
            handle_blocked_popup(driver)
            touch_outside(driver)

            button_upload = wait.until(
                expected.element_to_be_clickable((
                    By.ID, "com.getplus.application:id/btn_upload_receipt")))
            button_upload.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print('==========================ALL SR ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT========='
                  '=================')

            navigate_back = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ACCESSIBILITY_ID, "Navigate up")))
            navigate_back.click()

        with allure.step("Validate blocked popup in Eshop feature"):
            # Eshop page blocked popup
            eshop_index = 1
            eshop = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, "//*[@resource-id='com.getplus.application:id/ll_card_icon'][position()={}]"
                    .format(eshop_index + 1)
                )))
            eshop.click()
            time.sleep(2)

            # sampling thumbnail, later will add all thumbnail index
            guest_xpath.eshop_thumb_index(1)
            handle_blocked_popup(driver)
            touch_outside(driver)
            guest_xpath.eshop_thumb_index(2)
            handle_blocked_popup(driver)
            touch_outside(driver)

            eshop_banner = wait.until(
                expected.presence_of_element_located((
                    By.ID, "com.getplus.application:id/iv_slider")))
            eshop_banner.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("==========================ESHOP ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT==========================")
            touch_back(driver)

        with allure.step("Validate blocked popup in Convert feature"):
            convert_index = 2
            convert = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, "//*[@resource-id='com.getplus.application:id/ll_card_icon'][position()={}]"
                    .format(convert_index + 1)
                )))
            convert.click()

            elements_to_test = ["Reward BCA",
                                "G CARD",
                                "airasia rewards",
                                "KrisFlyer miles",
                                "MAPCLUB Points",
                                "Mil.K"]
            guest_android_automator = GuestAndroidUiAutomator(driver)
            for element_text in elements_to_test:
                guest_android_automator.handle_convert(element_text)

            # Garuda need to scroll down to be element present on screen
            scroll(driver)
            garuda = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("GarudaMiles")'
                ))
            )
            garuda.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("==========================CONVERT ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT==="
                  "=======================")
            touch_back(driver)

        ''' -> survey hide
        with allure.step("Validate blocked popup in Survey feature"):
            survey_index = 3
            survey = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, "//*[@resource-id='com.getplus.application:id/ll_card_icon'][position()={}]"
                    .format(survey_index + 1)
                )))
            survey.click()
            handle_blocked_popup(driver)
            print("==========================SURVEY ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=========="
                  "================")
            touch_outside(driver)
        '''

        with allure.step("Validate blocked popup in Beli poin feature"):
            belipoin_index = 3
            belipoin = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, "//*[@resource-id='com.getplus.application:id/ll_card_icon'][position()={}]"
                    .format(belipoin_index + 1)
                )))
            belipoin.click()
            handle_blocked_popup(driver)
            print("=========================BELI POIN ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=="
                  "=======================")
            touch_outside(driver)

        with allure.step("Validate blocked popup in Gift code feature"):
            giftcode_index = 4
            gift_code = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, "//*[@resource-id='com.getplus.application:id/ll_card_icon'][position()={}]"
                    .format(giftcode_index + 1)
                )))
            gift_code.click()
            handle_blocked_popup(driver)
            print("=========================GIFT CODE ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT======= "
                  "==================")
            touch_outside(driver)

        with allure.step("Validate blocked popup in Produk feature"):
            produk = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView").text("Produk")'
                )))
            produk.click()
            try:
                time.sleep(4)
                onboarding_helper.touch_hold()
                handle_airship_reward = HandleAirshipElement()
                handle_airship_reward.start(driver)
            except TimeoutException:
                print("Marketing reward did not appear. Continuing with the rest of the test.")
            # Assert the blocked popup by product offer in each tab category
            semua_produk = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                    "android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/"
                                    "android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[1]/"
                                    "android.view.ViewGroup/android.widget.ImageView"))
            )
            semua_produk.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            groceries = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Groceries"]/android.widget.TextView'
                )))
            groceries.click()
            time.sleep(2)
            groceries_produk = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                    "android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/"
                                    "android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[1]/"
                                    "android.view.ViewGroup/android.widget.ImageView"
                )))
            groceries_produk.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            touch_back(driver)

            lifestyle = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Lifestyle"]/android.widget.TextView'
                )))
            lifestyle.click()
            time.sleep(2)
            lifestyle_produk = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                    "android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/"
                                    "android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[2]/"
                                    "android.view.ViewGroup/android.widget.ImageView"
                )))
            lifestyle_produk.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            touch_back(driver)

            retail = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Retail"]/android.widget.TextView'

                )))
            retail.click()
            time.sleep(2)
            retail_produk = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                    "android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/"
                                    "android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[3]/"
                                    "android.view.ViewGroup/android.widget.ImageView"
                )))
            retail_produk.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            touch_back(driver)

            # Assert from more filter
            more_filter = wait.until(
                expected.element_to_be_clickable((
                    By.ID, "com.getplus.application:id/ib_filter")))
            more_filter.click()

            food_beverages = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("Foods and Beverages")'
                )))
            food_beverages.click()
            time.sleep(2)
            food_beverages_produk = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                    "android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/"
                                    "android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[4]/"
                                    "android.view.ViewGroup/android.widget.ImageView"
                )))
            food_beverages_produk.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=========================PRODUK ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=========================")
            touch_back(driver)
            time.sleep(2)
            back(driver)

        time.sleep(2)

        with allure.step("Validate blocked popup in Evoucher feature"):
            evoucher = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("eVoucher")'
                )))
            evoucher.click()
            evoucher_semua = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                    "android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/"
                                    "android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[1]/"
                                    "android.view.ViewGroup/android.widget.ImageView"
                )))
            evoucher_semua.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            groceries = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Groceries"]/android.widget.TextView'
                )))
            groceries.click()
            time.sleep(2)
            groceries_evoucher = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/'
                                    'android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[2]/'
                                    'android.view.ViewGroup/android.widget.ImageView'
                )))
            groceries_evoucher.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            touch_back(driver)

            lifestyle = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Lifestyle"]/android.widget.TextView'
                )))
            lifestyle.click()
            time.sleep(2)
            lifestyle_evoucher = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/'
                                    'android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[3]/'
                                    'android.view.ViewGroup/android.widget.ImageView'
                )))
            lifestyle_evoucher.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            touch_back(driver)

            retail = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Retail"]/android.widget.TextView'
                )))
            retail.click()
            time.sleep(2)
            retail_evoucher = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/'
                                    'android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[4]/a'
                                    'ndroid.view.ViewGroup/android.widget.ImageView'
                )))
            retail_evoucher.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            touch_back(driver)

            more_filter = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/ib_filter'
                )))
            more_filter.click()
            more_filter_evoucher = wait.until(
                expected.presence_of_element_located((
                        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                      '.text("Beauty and Wellness")'
                )))
            more_filter_evoucher.click()
            beauty_wellnes = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/'
                                    'android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[3]/'
                                    'android.view.ViewGroup/android.widget.ImageView'
                )))
            beauty_wellnes.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=========================EVOUCHER ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT==========="
                  "==============")
            touch_back(driver)
            time.sleep(2)
            back(driver)

        with allure.step("Validate blocked popup in Donasi feature"):
            # Donasi guest account
            donasi = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView").text("Donasi")'
                )))
            donasi.click()
            time.sleep(2)
            donasi_banner = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/'
                                    'androidx.recyclerview.widget.RecyclerView[1]/android.widget.FrameLayout[1]/'
                                    'android.view.ViewGroup/android.widget.ImageView'
                )))
            donasi_banner.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            donasi_campaign = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/'
                                    'androidx.recyclerview.widget.RecyclerView[2]/android.widget.FrameLayout[1]/'
                                    'android.view.ViewGroup'
                )))
            donasi_campaign.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=========================DONASI ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=========================")
            touch_back(driver)

        with allure.step("Validate blocked popup in Ewallet feature"):
            # Ewallet guest account
            ewallet = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("eWallet")'
                )))
            ewallet.click()
            dana = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView").text("DANA")'
                )))
            dana.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            linkaja = wait.until(
                expected.element_to_be_clickable((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("LinkAja")'
                )))
            linkaja.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=========================EWALLET ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=========================")
            touch_back(driver)

        with allure.step("Validate blocked popup in Message center feature"):
            # Message center
            message_center = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/iv_notification')))
            message_center.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=======================MESSAGE CENTER ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=================="
                  "=====")

        with allure.step("Validate blocked popup in Riwayat poin feature"):
            # User info card
            riwayat_poin = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("Lihat poin")'
                ))
            )
            riwayat_poin.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("========================RIWAYAT POIN ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT==============="
                  "=========")

        with allure.step("Validate blocked popup in QRIS feature"):
            qris = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("QRIS")'
                ))
            )
            qris.click()
            blu = wait.until(
                expected.visibility_of_element_located((
                    AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.getplus.application:id/'
                                    'iv_merchant_banner"])[1]'))
            )
            blu.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("========================QRIS ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT==============="
                  "=========")

        with allure.step("Validate blocked popup in Gunakan voucher feature"):
            voucher_gunakan = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("Gunakan")'
                ))
            )
            voucher_gunakan.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=======================GUNAKAN VOUCHER ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT============="
                  "==========")

        with allure.step("Validate blocked popup in Promo banner homepage and promo page feature"):
            # Homepage section
            promo_banner = wait.until(
                expected.presence_of_element_located((
                    By.ID, 'com.getplus.application:id/banner_image')))
            promo_banner.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("========================SLIDER BANNER ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=========="
                  "==============")

            lihat_semua_promo = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/tv_promo_see_all'))
            )
            lihat_semua_promo.click()
            promo = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/tv_period')))
            promo.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=========================PROMO BANNER ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT========="
                  "================")
            touch_back(driver)

        with allure.step("Validate blocked popup in Gamification feature"):
            gamification = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/my_image_view')))
            gamification.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("========================GAMIFICATION ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=============="
                  "==========")

        scroll_homepage(driver)
        with allure.step("Validate blocked popup in Getplus travel feature"):
            getplus_travel = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/iv_merchant_home')))
            getplus_travel.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=======================GETPLUS TRAVEL ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT========"
                  "===============")

        with allure.step("Validate blocked popup in Navigation bar feature"):
            # Navbar assertion blocked popup
            foto_struk = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/fab_foto_struk')))
            foto_struk.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            voucher_saya = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/nav_item_vouchers')))
            voucher_saya.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            myprofile = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/nav_item_mygetplus')))
            myprofile.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            print("=========================NAVBAR ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT=========================")

        with allure.step("Validate blocked popup in Merchant feature"):
            # Merchant assertion blocked popup from homepage
            merchant_homepage = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/iv_merchant_home'
                )))
            merchant_homepage.click()
            handle_blocked_popup(driver)
            touch_outside(driver)

            # Merchant assertion blocked popup from homepage - lihat semua
            merchant_homepage_lihat_semua = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/tv_merchant_home_see_all'
                )))
            merchant_homepage_lihat_semua.click()
            merchant_homepage_lihat_semua_click = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/'
                                    'android.widget.ScrollView/android.view.ViewGroup/'
                                    'androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/'
                                    'android.view.View'
                )))
            merchant_homepage_lihat_semua_click.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            back_button = wait.until(
                expected.element_to_be_clickable((By.ID, 'com.getplus.application:id/iv_back')))
            back_button.click()

            # Merchant assertion blocked popup from merchant nav bar (merchant terbaru & category)
            merchant_navbar = wait.until(
                expected.element_to_be_clickable((By.ID, 'com.getplus.application:id/nav_item_merchant')))
            merchant_navbar.click()
            time.sleep(2)
            merchant_terbaru = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/'
                                    'android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView[1]/'
                                    'android.view.ViewGroup[1]/android.widget.ImageView'
                )))
            merchant_terbaru.click()
            handle_blocked_popup(driver)
            touch_outside(driver)
            merchant_category = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'
                                                  '.text("Food And Beverages")'
                )))
            merchant_category.click()
            time.sleep(2)
            merchant_category_click = wait.until(
                expected.presence_of_element_located((
                    AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/'
                                    'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                                    'android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/'
                                    'android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/'
                                    'android.view.ViewGroup[1]'
                )))
            merchant_category_click.click()
            handle_blocked_popup(driver)
            print("========================ALL MERCHANT ENTRY POINT WAS BLOCKED FOR GUEST ACCOUNT============="
                  "===========")

            time.sleep(2)

    except Exception as e:
        # Handle the failed assertion
        allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
        raise AssertionError("Assertion failed: {}".format(str(e)))


@allure.epic("Test Case Login as Guest")
@allure.story("As a user, i have registered account and want to login from guest login")
@allure.description("This test to validate existing account login from blocked popup guest account")
@allure.tag("Android", "5.1.0",)
@allure.label("owner", "Arlingga")
@allure.title("Validate login from blocked pop up guest account")
def test_login_from_guest(driver):
    wait = WebDriverWait(driver, 30)
    try:
        test_guest_login(driver, click_lewati_button=True)
        myprofile = wait.until(
            expected.element_to_be_clickable((
                By.ID, 'com.getplus.application:id/nav_item_mygetplus')))
        myprofile.click()
        with allure.step("Go to login page"):
            blocked_popups = wait.until(
                expected.element_to_be_clickable((
                    By.ID, 'com.getplus.application:id/tv_secondary_cta')))
            blocked_popups.click()

        with allure.step("Login with valid email"):
            from test.GetPlus_login_rebuild import TestLogin
            guest_test_login = TestLogin()
            guest_test_login.test_valid_login(driver, assertion_flow=False)

        time.sleep(3)

    except Exception as e:
        # Handle the failed assertion
        allure.attach(driver.get_screenshot_as_png(), name="screenshot_failed_assertion",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="exception", attachment_type=allure.attachment_type.TEXT)
        raise AssertionError("Assertion failed: {}".format(str(e)))
