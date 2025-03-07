import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_base_page_color(driver):
    driver.get('http://localhost:8000')
    body_color = driver.find_element(By.TAG_NAME, "body").value_of_css_property("background-color")
    expected_color = 'rgba(48, 48, 166, 1)'
    assert body_color == expected_color
