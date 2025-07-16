from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.ui import WebDriverWait

def get_driver():
    return BuiltIn().get_library_instance("SeleniumLibrary").driver

def get_wait(timeout=20):
    driver = get_driver()
    return WebDriverWait(driver, timeout)
