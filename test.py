from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_instagram_post_info(post_url):
    # Initialize WebDriver (make sure you've downloaded chromedriver and it's in PATH)
    driver = webdriver.Chrome()

    try:
        driver.get(post_url)
        time.sleep(5)  # Wait for post to load

        # Extract author
        meta_description = driver.find_element(By.XPATH, "//meta[@name='description']")
        description_content = meta_description.get_attribute('content')

        print("Meta description content:")
        print(description_content)

    finally:
        driver.quit()

if __name__ == '__main__':
    input_url = input("Enter the Instagram post URL: ")
    post_info = get_instagram_post_info(input_url)
    print(post_info)