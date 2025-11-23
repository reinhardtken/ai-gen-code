from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def search_baidu(keyword):
    # Configurable paths for Chrome and ChromeDriver
    path_ChromeDriver = "C:/prog/chromedriver/chromedriver-win64/chromedriver.exe"
    path_Chrome = "C:/prog/chromedriver/chrome-win64/chrome.exe"
    
    # Set up Chrome options to address sandbox and other issues
    chrome_options = Options()
    chrome_options.binary_location = path_Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")  # Disable JS to reduce errors
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--mute-audio")
    
    # Create service with ChromeDriver path
    service = Service(path_ChromeDriver)
    
    try:
        # Initialize Chrome driver with specified paths and options
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome driver initialized successfully")
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        print("Please check your Chrome and ChromeDriver paths")
        return
    
    try:
        # Open Baidu website
        driver.get("https://www.baidu.com")
        print("Successfully opened Baidu")
        
        # Give the page some time to load completely
        time.sleep(2)
        
        # Find the search input field by its ID
        search_box = driver.find_element(By.ID, "kw")
        print("Found search box")
        
        # Enter the search keyword
        search_box.send_keys(keyword)
        print(f"Entered keyword: {keyword}")
        
        # Submit the search by pressing Enter
        search_box.send_keys(Keys.RETURN)
        print("Submitted search")
        
        # Wait for results to load
        time.sleep(5)
        
        # Print the title of the results page
        print(f"Page title: {driver.title}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    search_baidu("你好")