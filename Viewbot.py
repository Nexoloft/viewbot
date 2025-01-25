import threading
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Configure the proxy
PROXY = ""  # Proxy address with authentication

# List of links to open
links = [
    ""
    
]

def setup_driver():
    """Set up the Selenium WebDriver with proxy settings and mimic human behavior."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, "chromedriver")  # Assuming chromedriver is in the same folder

    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("useAutomationExtension", False)

    # Randomize window size
    # width = random.randint(375, 414)  # Typical iPhone widths
    # height = random.randint(667, 896)  # Typical iPhone heights
    # chrome_options.add_argument(f'--window-size={width},{height}')
    # Set proxy
    chrome_options.add_argument(f'--proxy-server={PROXY}')
    # headless
    #chrome_options.add_argument("--headless")
    
    # Create the driver
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    
    return driver


def open_link():
    """Open a random link using Selenium, wait for page load, and click an element."""
    driver = setup_driver()
    try:
        while True:
            link = random.choice(links)
            print(f"Opening link: {link}")
            driver.get(link)  # Open the link
            
            #Wait for the page to load and the button to be clickable
            try:
                print("Waiting for the button to be clickable...")
                wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds
                button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="movie_player"]/div[7]/button')))
                print("Button is clickable. Clicking the button now.")
                button.click()  # Click the button
            except Exception as e:
                print(f"Failed to click the button: {e}")
            sleep_time = random.randint(600, 720)
            print(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)  # Wait for the specified time
            print(f"Closing the browser for link: {link}")
            driver.delete_all_cookies()  # Clear cookies (optional, for fresh browsing)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

# Number of threads
num_threads = 1

# Create threads to open links
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=open_link)
    threads.append(thread)
    thread.start()
    # Sleep for 0.5 second to avoid opening all links at the same time
    time.sleep(30)

# Join threads to keep the program running
for thread in threads:
    thread.join()
