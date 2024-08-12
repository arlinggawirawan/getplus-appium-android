from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from config.conftest import driver


class GuestXpath:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def banner_scan_receipt_index(self, index):
        # Construct the XPath using the index
        xpath = (f"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                 f"android.widget.FrameLayout/android.widget.LinearLayout/"
                 f"android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/"
                 f"android.view.ViewGroup/android.widget.RelativeLayout/"
                 f"androidx.viewpager.widget.ViewPager/"
                 f"androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[{index}]")
        banner_struk = self.wait.until(
            expected.element_to_be_clickable((
                AppiumBy.XPATH, xpath
            ))
        )
        banner_struk.click()

    def merchant_scan_receipt_index(self, index):
        xpath = (f"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                 f"android.widget.FrameLayout/android.widget.LinearLayout/"
                 f"android.widget.FrameLayout/android.view.ViewGroup/"
                 f"android.widget.ScrollView/android.view.ViewGroup/"
                 f"android.widget.GridView/android.view.ViewGroup[{index}]/android.widget.ImageView")
        merchant_sr = self.wait.until(
            expected.element_to_be_clickable((
                AppiumBy.XPATH, xpath
            ))
        )
        merchant_sr.click()

    def eshop_thumb_index(self, index):
        xpath = (f"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                 f"android.widget.FrameLayout/android.widget.LinearLayout/"
                 f"android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/"
                 f"android.view.ViewGroup/android.widget.GridView/android.view.ViewGroup[{index}]/"
                 f"android.widget.FrameLayout/android.widget.ImageView")
        eshop_thumb = self.wait.until(
            expected.element_to_be_clickable((
                AppiumBy.XPATH, xpath
            ))
        )
        eshop_thumb.click()

    