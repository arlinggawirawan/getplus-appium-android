from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
import pytest

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'


@pytest.fixture(scope='session')
def appium_service():
    service = AppiumService()
    service.start(
        # Check the output of `appium server --help` for the complete list of
        # server command line arguments
        args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)],
        timeout_ms=20000,
    )
    yield service
    service.stop()


@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'android'
    options.device_name = 'uiautomator2'
    options.app_package = 'com.getplus.application'
    options.app_activity = 'com.getplus.auth.login.views.activity.LoginActivity'
    driver = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driver_onboarding():
    options = UiAutomator2Options()
    options.platform_name = 'android'
    options.device_name = 'uiautomator2'
    options.app_package = 'com.getplus.application'
    options.app_activity = 'com.getplus.onboarding.ui.activity.OnboardingActivity'
    driver = webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)
    yield driver
    driver.quit()
