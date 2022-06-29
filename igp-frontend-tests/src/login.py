import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located as located
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from response import info, testing, success, fail, error


def instance_login(portals):
    for portal in portals:
        portal_login(portal)


def portal_login(portal):
    def close_browser():
        driver.close()
        driver.quit()

    def get_by(by):
        if by.upper() == "XPATH":
            return By.XPATH
        return By.ID

    def do(action, action_name, wait_time, by, field, value=None):
        # info(f"{action}, {action_name}, {wait_time}, {by}, {field}, {value}")
        try:
            wait = WebDriverWait(driver, wait_time)
            wait.until(located((by, field)))
            sleep(1)

            if action == "click":
                if portal_name == "CasinoVoila":
                    driver.execute_script("arguments[0].click();", driver.find_element(by, field))
                else:
                    driver.find_element(by, field).click()
            elif action == "send":
                driver.find_element(by, field).send_keys(value)
            elif action == "check":
                if driver.find_element(by, field):
                    success(f"{portal_name} {action_name} is working properly.")
                else:
                    fail(f"{portal_name} {action_name} doesn't work (error).")
            else:
                fail(f"Unsupported action {action}. Action has to be 'click', 'send' or 'check'.")

        except TimeoutException:
            fail(f"{portal_name} {action_name} doesn't work (timeout).")

        except ElementClickInterceptedException as e:
            error(f"{e} is not clickable.")

        except ElementNotInteractableException as e:
            error(f"{e} is not interactable.")

    def accept_cookie():
        try:
            ca = portal["cookie_accept"]
            do("click", "cookie accept button", 15, get_by(ca["by"]), ca["property"])

        except KeyError as e:
            error(f"Invalid configuration for {e}. Check config details and restart to try again.")

    def login():
        try:
            # Step 1. - Wait for Login button to appear and click on Login button
            lb = portal["login_button"]
            do("click", "login button", 15, get_by(lb["by"]), lb["property"])

            # Step 2. - Insert username in the box
            ub = portal["username_box"]
            do("send", "username box", 15, get_by(ub["by"]), ub["property"], portal["username"])

            # Step 3. - Insert password in the box
            pb = portal["password_box"]
            do("send", "password box", 15, get_by(pb["by"]), pb["property"], portal["password"])

            # Step 4. - Click on Sign in button
            sb = portal["submit_button"]
            do("click", "submit button", 15, get_by(sb["by"]), sb["property"])

        except KeyError as e:
            error(f"Invalid configuration for {e}. Check config details and restart to try again.")

    def login_check():
        try:
            user_avatar = portal["user_avatar"]
            # If user_avatar is not specified, check cashier modal
            logged_in = user_avatar if user_avatar else portal["cashier_modal"]

            do("check", "login", 15, get_by(logged_in["by"]), logged_in["property"])

        except KeyError as e:
            error(f"Invalid configuration for {e}. Check config details and restart to try again.")

    def cashier_check():
        try:
            # If user_avatar exists we don't need to check for cashier modal
            if portal["user_avatar"]:
                return

            db = portal["deposit_button"]
            do("check", "cashier", 15, get_by(db["by"]), db["property"])

        except KeyError as e:
            error(f"Invalid configuration for {e}. Check config details and restart to try again.")

    service = Service(ChromeDriverManager(log_level=logging.WARNING).install())

    options = Options()
    # options.headless = True  # Runs Chrome in headless mode.

    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    try:
        portal_name = portal["name"]
        testing(f"{portal_name} login.")

        # Step 1. - Getting the desired page that we are going to test
        driver.get(portal["url"])
        sleep(5)

        # Step 2. - Wait for cookie accept button to appear and click it
        accept_cookie()

        # Step 3. - Input credentials and click submit button
        login()

        # Step 4. - Wait for user avatar or cashier modal to appear to know we are signed in
        login_check()

        # Step 5. - In case there is no user avatar, check existence of deposit button in cashier modal
        cashier_check()

    except KeyError as ke:
        error(f"Invalid configuration for {ke}. Check config details and restart to try again.")

    except TimeoutException as te:
        error(f"Timeout for {te}. Check portal manually or try again.")

    finally:
        info("---------------------------------------------------------------------")
        close_browser()
