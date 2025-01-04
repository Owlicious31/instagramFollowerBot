import time
import logging

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#For type annotations
from selenium.webdriver.remote.webelement import WebElement

from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

from site_info import InstaSiteInfo

logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s - %(asctime)s")

class InstagramBot:

    def __init__(self,target_acc: str,number_to_follow: int) -> None:

        self.target_account: str = target_acc
        self.number_to_follow: int = number_to_follow

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option(name="detach", value=True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

        logging.info("Initialized Instagram bot")


    def login_to_instagram(self,email: str,password: str) -> None:
        """
        Login to Instagram.
        :param email: The email connected to your Instagram account.
        :param password: The password for your Instagram Account.
        :return: None
        """
        try:
            logging.info("Logging in")

            self.driver.get(InstaSiteInfo.URL)

            if "Instagram" not in self.driver.title:
                logging.error("Was not directed to Instagram login page, ensure url is correct.")
                raise Exception("Unable to find Instagram login page.")

            wait = WebDriverWait(driver=self.driver,timeout=10)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,InstaSiteInfo.LOGIN_BUTTON)))

            email_input: WebElement = self.driver.find_element(By.NAME,InstaSiteInfo.EMAIL_INPUT_NAME)
            email_input.send_keys(email)

            password_input: WebElement = self.driver.find_element(By.NAME,InstaSiteInfo.PASSWORD_INPUT_NAME)
            password_input.send_keys(password)

            login_button: WebElement = self.driver.find_element(By.CSS_SELECTOR,InstaSiteInfo.LOGIN_BUTTON)
            login_button.click()

            wait.until(ec.presence_of_element_located((By.XPATH,InstaSiteInfo.SAVE_INFO_BUTTON)))

            save_info_button: WebElement = self.driver.find_element(By.XPATH,InstaSiteInfo.SAVE_INFO_BUTTON)
            save_info_button.click()

            logging.info("Login Succeeded")

            time.sleep(2)

        except NoSuchElementException:
            logging.error("Error getting element on login page. Page layout may have changed.")
            raise

        except TimeoutException:
            logging.error("Could not find log in button, timed out.")
            raise

        except Exception as e:
            logging.error(f"Error logging in: {e}")
            raise


    def find_followers(self) -> None:
        """
        Find the followers page of your target account.
        :return: None
        """
        try:
            logging.info("Navigating to target account's page.")

            self.driver.get(f"{InstaSiteInfo.URL}/{self.target_account}")

            followers_selector: str = InstaSiteInfo.FOLLOWERS_LINK_TEMPLATE.replace("placeholder", self.target_account)

            wait = WebDriverWait(driver=self.driver,timeout=10)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,followers_selector)))

            followers_link: WebElement = self.driver.find_element(By.CSS_SELECTOR,value=followers_selector)
            followers_link.click()

            logging.info("Retrieved followers")

        except NoSuchElementException:
            logging.error("Error finding followers. Ensure you are signed in and the FOLLOWERS_LINK is correct.")
            raise

        except StaleElementReferenceException:
            logging.error("Error finding followers. The follower link's info might have changed before it was clicked.")
            raise

        except TimeoutException:
            logging.error("Timed out: could not find followers link.")
            raise

        except Exception as e:
            logging.error(f"Error finding followers: {e}")
            raise


    def follow_followers(self) -> None:
        """
        Follow the followers of your target account.
        :return: None
        """
        try:
            wait = WebDriverWait(driver=self.driver,timeout=10)
            wait.until(ec.presence_of_element_located((By.XPATH,InstaSiteInfo.FOLLOW_BUTTONS)))

            for i in range(self.number_to_follow):
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight",
                    InstaSiteInfo.FOLLOW_BUTTONS
                )
                time.sleep(0.5)

            follow_buttons: list[WebElement] = self.driver.find_elements(By.XPATH, value=InstaSiteInfo.FOLLOW_BUTTONS)
            follow_buttons = follow_buttons[:self.number_to_follow]

            for i,button in enumerate(follow_buttons):
                time.sleep(2)

                self.driver.execute_script("arguments[0].click();", button)

                logging.info(f"Followed follower: {i + 1}")

                time.sleep(2)

            logging.info("Finished Following. Closing program...")

        except TimeoutException:
            logging.error("Was unable to find follow buttons. Timed out. Ensure you were directed to the followers popup")
            raise

        except NoSuchElementException:
            logging.error("Was unable to find follower buttons. No such elements. Ensure you were redirected to the correct page")

        finally:
            self.driver.quit()
