from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def create_driver() -> webdriver:
    """:returns working webdriver to use for testing"""
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')
    wdriver = webdriver.Chrome(executable_path='chromedriver', options=op)
    return wdriver


def get_page(wdriver: webdriver, link: str) -> list:
    """
    Gets the page, clicks on an anchor
    :returns 50 steam comments"""
    wdriver.get(link)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'commentthread_allcommentslink')))

    wdriver.find_element(by=By.CLASS_NAME, value='commentthread_allcommentslink').click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'commentthread_comment_text')))

    return [x.text for x in wdriver.find_elements(by=By.CLASS_NAME, value='commentthread_comment_text')]


if __name__ == '__main__':
    """
        Program that returns the first 50 comments of a steam profile
    """
    driver = create_driver()
    comments = get_page(driver, 'https://steamcommunity.com/id/Abelitoo/')
    print(comments)
