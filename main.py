import os
import logging
from enum import Enum
from dotenv import load_dotenv

from bot import InstagramBot

logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s - %(asctime)s")

ENVIRONMENT = "DEMO"

if ENVIRONMENT == "DEMO":
    load_dotenv(".env.demo")
else:
    load_dotenv()

class EnvVars(Enum):
    EMAIL = os.getenv("INSTAGRAM_EMAIL")
    PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

def load_env_variables():
    """
    Load Environment variables
    :return: None
    """
    vars_loaded = True

    for var in EnvVars:
        if not var:
            logging.error(f"Could not find environment variable: {var.name}")
            vars_loaded = False

    if not vars_loaded:
        raise Exception("Was unable to load some environment variables")


def main() -> None:
    """
    Main function. Initialize the Instagram bot and follow followers.
    :return: None
    """

    bot = InstagramBot(target_acc="chefsteps",number_to_follow=10)
    bot.login_to_instagram(email=EnvVars.EMAIL.value,password=EnvVars.EMAIL.value)
    bot.find_followers()
    bot.follow_followers()

if __name__ == '__main__':
    main()
