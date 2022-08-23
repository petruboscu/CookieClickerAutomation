import time

from selenium import webdriver

from automation import CookieClicker
from paths import cookie_clicker_path as c_c_path


def set_up_automation(path=c_c_path) -> CookieClicker:
    """The set_up_automation function is responsible for the initial phase of the automation,
     it's opening and the clicking of some one time pop-ups, it also checks that the run_automation function can start"""
    driver = webdriver.Chrome()
    driver.get(path)

    automation = CookieClicker(driver)

    automation.wait_to_load()
    automation.allow_cookies_button.click()
    automation.language_en.click()
    automation.wait_to_load()

    assert automation.cookies == 0, "Start-Up Failed"

    return automation


def run_automation(automation: CookieClicker, product_index=2, upgrade=100):
    """The whole automation is pretty much condensed here
        Step by step:
            - the automation gets the prices of the products and chooses the smallest one
            - the automation clicks the 'Big Cookie' until the price of the cheapest upgrade has been reached
            - the automation clicks the corresponding product
            - The automation increases the product range and closes the notifications
              if a more expensive upgrade was bought

        The automation stops when you close the browser.
    """
    try:
        while True:
            price, number = automation.get_price_of_next_purchase(product_index, upgrade)
            automation.click_big_cookie_until_upgrade(price)
            if number != -1:
                automation.product(number).click()
            else:
                automation.upgrade.click()
                upgrade = automation.get_upgrade_price()
            if product_index - number < 2:
                product_index += 1
                automation.close_notifications_button.click()
    except:
        if automation.not_yet_implemented:
            return
        try:
            upgrade = automation.get_upgrade_price()
            run_automation(automation, product_index, upgrade)
        except Exception as ex:
            print('Session was stopped.')


def main():
    """The main function that uses set_up_automation() and run_automation() functions"""
    start_time = time.time()
    automation = set_up_automation()
    run_automation(automation)
    if automation.not_yet_implemented:
        print('The Automation has reached an unimplemented feature.')
    print(f'The Automation has played Cookie Clicked for {round((time.time() - start_time) / 60)} minutes.')
    automation.driver.quit()
