import os
import logging
from dotenv import load_dotenv

from bot import InstagramBot

logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s - %(asctime)s")

ENVIRONMENT = "DEMO"

if ENVIRONMENT == "DEMO":
    load_dotenv(".env.demo")
else:
    load_dotenv()


def load_env_variables() -> dict[str,str]:
    """
    Load Environment variables
    :return: None
    """
    vars_loaded: bool = True

    email: str = os.getenv("INSTAGRAM_EMAIL")
    password: str = os.getenv("INSTAGRAM_PASSWORD")

    env_vars: dict = {
        "INSTAGRAM_EMAIL":email,
        "INSTAGRAM_PASSWORD":password,
    }

    for name,var in env_vars.items():
        if not var:
            logging.error(f"Could not find environment variable: {name}")
            vars_loaded = False

    if not vars_loaded:
        raise Exception("Was unable to load some environment variables")

    return env_vars


def main() -> None:
    """
    Main function. Initialize the Instagram bot and follow followers.
    :return:
    """
    env_vars: dict = load_env_variables()

    email: str = env_vars["INSTAGRAM_EMAIL"]
    password: str = env_vars["INSTAGRAM_PASSWORD"]

    bot = InstagramBot(target_acc="chefsteps",number_to_follow=10)
    bot.login_to_instagram(email=email,password=password)
    bot.find_followers()
    bot.follow_followers()

if __name__ == '__main__':
    main()
