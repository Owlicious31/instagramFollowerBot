class InstaSiteInfo:
    URL = "https://www.instagram.com"
    EMAIL_INPUT_NAME = "username"
    PASSWORD_INPUT_NAME = "password"
    LOGIN_BUTTON = "button[type='submit']"
    SAVE_INFO_BUTTON = "//button[text()='Save info']"
    FOLLOWERS_LINK_TEMPLATE = 'a[href="/placeholder/followers/"]'
    FOLLOW_BUTTONS = "//div[text()='Follow']/../.."
    FOLLOWERS_POPUP = "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"