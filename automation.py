from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CookieClicker:
    default_wait_time = 20

    one_million = 1_000_000
    one_billion = 1_000_000_000
    one_trillion = 1_000_000_000_000

    def __init__(self, driver):
        self.driver = driver
        self.not_yet_implemented = False
        self.wait_action = ActionChains(driver).pause(3)

    """Locators Used for the automation"""

    language_en_locator = '//*[@id="langSelect-EN"]'
    allow_cookies_button_locator = '//*[@class="cc_btn cc_btn_accept_all"]'

    big_cookie_locator = '//*[@id="bigCookie"]'
    cookies_locator = '//div[@id="cookies"]'

    upgrade_locator = '//*[@id="upgrade0"]'
    upgrade_price_locator = '//div[@id="tooltipAnchor"]//div[@id="tooltip"]//span[@class="price" or @class="price disabled"]'

    @staticmethod
    def product_locator(number) -> str:
        return f'//div[@id="product{number}"]'

    @staticmethod
    def product_price_locator(number) -> str:
        return f'//div[@id="product{number}"]//span[@id="productPrice{number}"]'

    close_notifications_button_locator = '//div[@class="framed close sidenote"]'

    """Wait functions implemented for stability purposes"""

    def wait_to_load(self, time=default_wait_time):
        try:
            _ = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((By.XPATH, self.big_cookie_locator)))
            _ = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((By.XPATH, self.cookies_locator)))
        except:
            raise Exception(f'Page did not load correctly.')
        self.wait_action.perform()

    def wait_for_and_return_web_element(self, locator: str, time):
        try:
            element = WebDriverWait(self.driver, time). \
                until(EC.presence_of_element_located((By.XPATH, locator)))
            return element
        except:
            raise Exception(f'Locator "{locator}" did not appear in {time} seconds.')

    """Web elements returned by the driver and used as @property methods by the class"""

    @property
    def language_en(self, time=default_wait_time):
        return self.wait_for_and_return_web_element(self.language_en_locator, time)

    @property
    def allow_cookies_button(self, time=default_wait_time):
        return self.wait_for_and_return_web_element(self.allow_cookies_button_locator, time)

    @property
    def close_notifications_button(self, time=default_wait_time):
        return self.wait_for_and_return_web_element(self.close_notifications_button_locator, time)

    @property
    def big_cookie(self, time=default_wait_time):
        return self.wait_for_and_return_web_element(self.big_cookie_locator, time)

    @property
    def cookies(self, time=default_wait_time) -> int:
        cookies_text = self.wait_for_and_return_web_element(self.cookies_locator, time).text.split()
        cookies = cookies_text[0].replace(',', '')
        unit = cookies_text[1]
        if cookies.isdigit() and (unit == 'cookies' or unit == 'cookie'):
            return int(cookies)
        elif unit == 'million':
            return int(float(cookies) * self.one_million)
        elif unit == 'billion':
            return int(float(cookies) * self.one_billion)
        elif unit == 'trillion':
            return int(float(cookies) * self.one_trillion)
        else:
            self.not_yet_implemented = True
            raise Exception("This Feature is not implemented, Values don't go higher than trillions yet")

    @property
    def upgrade(self, time=default_wait_time):
        return self.wait_for_and_return_web_element(self.upgrade_locator, time)

    @property
    def upgrade_price(self, time=default_wait_time) -> int or None:
        price = self.wait_for_and_return_web_element(self.upgrade_price_locator, time).text.replace(',', '')
        if price.isdigit():
            return int(price)
        elif 'million' in price:
            return int(float(price.replace(' million', '')) * self.one_million)
        elif 'billion' in price:
            return int(float(price.replace(' billion', '')) * self.one_billion)
        elif 'trillion' in price:
            return int(float(price.replace(' trillion', '')) * self.one_trillion)
        else:
            return None

    def product(self, number: int, time=default_wait_time):
        return self.wait_for_and_return_web_element(self.product_locator(number), time)

    def product_price(self, number: int, time=15) -> int:
        price = self.wait_for_and_return_web_element(self.product_price_locator(number), time).text.replace(',', '')
        if price.isdigit():
            return int(price)
        elif 'million' in price:
            return int(float(price.replace(' million', '')) * self.one_million)
        elif 'billion' in price:
            return int(float(price.replace(' billion', '')) * self.one_billion)
        elif 'trillion' in price:
            return int(float(price.replace(' trillion', '')) * self.one_trillion)
        else:
            self.not_yet_implemented = True
            raise Exception("This Feature is not implemented, Values don't go higher than trillions yet")

    """Function needed for the automation process"""

    def get_upgrade_price(self, tries=10):
        try_action = ActionChains(self.driver)
        try_action.move_to_element(self.big_cookie).pause(1).move_to_element(self.upgrade).pause(2)

        upgrade = None
        for _ in range(tries):
            try:
                try_action.perform()
                upgrade = self.upgrade_price
                if upgrade is not None:
                    break
            except:
                self.wait_action.perform()
        return upgrade

    def get_price_of_next_purchase(self, product_index: int, upgrade):
        product_prices = [self.product_price(i) for i in range(product_index)]
        price = min(product_prices)
        if price <= upgrade:
            number = product_prices.index(price)
            return price, number
        else:
            return upgrade, -1

    def click_big_cookie_until_upgrade(self, price: int):
        for _ in range(price):
            self.big_cookie.click()
            if self.cookies >= price:
                break
