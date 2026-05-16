import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000")


@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    yield driver

    driver.quit()


def open_page(browser, path):
    browser.get(f"{BASE_URL}{path}")


def test_login_page_opens(browser):
    open_page(browser, "/login")

    assert "login" in browser.current_url.lower()
    assert browser.find_element(By.NAME, "email")
    assert browser.find_element(By.NAME, "password")


def test_register_page_opens(browser):
    open_page(browser, "/register")

    assert "register" in browser.current_url.lower()
    assert browser.find_element(By.NAME, "firstName")
    assert browser.find_element(By.NAME, "lastName")
    assert browser.find_element(By.NAME, "email")
    assert browser.find_element(By.NAME, "password")
    assert browser.find_element(By.NAME, "confirm-password")


def test_root_redirects_to_login(browser):
    open_page(browser, "/")

    WebDriverWait(browser, 5).until(EC.url_contains("/login"))
    assert "/login" in browser.current_url


def test_home_redirects_to_login_when_not_logged_in(browser):
    open_page(browser, "/home")

    WebDriverWait(browser, 5).until(EC.url_contains("/login"))
    assert "/login" in browser.current_url


def test_forum_redirects_to_login_when_not_logged_in(browser):
    open_page(browser, "/forum")

    WebDriverWait(browser, 5).until(EC.url_contains("/login"))
    assert "/login" in browser.current_url


def test_marketplace_redirects_to_login_when_not_logged_in(browser):
    open_page(browser, "/marketplace")

    WebDriverWait(browser, 5).until(EC.url_contains("/login"))
    assert "/login" in browser.current_url