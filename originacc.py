from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from config import *


def origin_login(email):
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1280, 768)
    wait = WebDriverWait(driver, 15)
    try:
        driver.get('https://www.origin.com')
        wait.until(EC.visibility_of_element_located((By.XPATH, './/origin-cta-login//a')))
        driver.find_element_by_xpath('.//origin-cta-login//a').click()
        login_window = driver.window_handles[1]
        driver.switch_to.window(login_window)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="email"]')))
        driver.find_element_by_xpath('//input[@id="email"]').send_keys(USER)
        driver.find_element_by_xpath('//input[@id="password"]').send_keys(PASSWORD)
        driver.find_element_by_xpath('//*[@id="content"]').click()
        driver.find_element_by_xpath('//a[@id="logInBtn"]').click()
        driver.switch_to.window(driver.window_handles[0])
        wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[text()="Sign In"]')))
        driver.find_element_by_xpath('//input[@ng-model="searchString"]').send_keys(email)
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH,
                                                         '//a[@class="otka otkc origin-friendtile-originId"]')))
            time.sleep(.5)
            driver.find_element_by_xpath('//a[@class="otka otkc origin-friendtile-originId"]/strong').click()
            time.sleep(5)
            nikcname = driver.find_element_by_xpath('//div[@class="otktitle-page origin-profile-header-username"]')
            img = driver.find_element_by_xpath('//div[@class="origin-profile-header-info-section"]/a/img')
            total = {
                'photo': img.get_attribute('src'), 'name': nikcname.text, 'url': driver.current_url
            }
            return total
        except:
            return 'Account not found'
    finally:
        driver.save_screenshot('screen_shot.png')
        driver.quit()


if __name__ == '__main__':
    print(origin_login)

