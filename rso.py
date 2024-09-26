from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import time
import random
import os

driver_path = '/opt/homebrew/bin/chromedriver'
forum_url = 'https://www.roforum.net/whats-new/posts/'

# Specify the Chrome profile settings
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-data-dir=/Users/jameswashkau/Library/Application Support/Google/Chrome/Default')
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def append_external_link(link):
    """Append extracted link to a file, excluding unwanted links."""
    if 'sld.one' not in link and 'javascript:' not in link:
        try:
            with open('external_links.txt', 'a') as f:
                f.write(link + '\n')
        except Exception as e:
            print(f"Error writing link to file: {e}")

def get_thread_links(driver):
    """Retrieve thread links from forum."""
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-tp-primary]:nth-of-type(1)'))
        )
        return [element.get_attribute('href') for element in elements]
    except TimeoutException:
        print("Timeout: Unable to find thread links.")
        return []
    except Exception as e:
        print(f"Error finding thread links: {e}")
        return []

def extract_external_links_from_thread(driver):
    """Extract external links from a thread as the page scrolls."""
    external_links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            post_contents = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.message-content'))
            )

            for content in post_contents:
                soup = BeautifulSoup(content.get_attribute('innerHTML'), 'html.parser')

                # Extracting links
                for link in soup.select('a[href^="http"]'):
                    href = link['href']
                    if 'roforum.net' not in href and href not in external_links:
                        append_external_link(href)
                        print(f"Link added: {href}")
                        external_links.add(href)

                # Extracting media
                for img in soup.select('img[src]'):
                    src = img['src']
                    if src not in external_links:
                        append_external_link(src)
                        print(f"Media added: {src}")
                        external_links.add(src)

            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 3))

            # Check scroll height to stop
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        except NoSuchElementException:
            print("Error: message-content elements not found.")
            break
        except TimeoutException:
            print("Timeout: Error extracting links.")
            break
        except Exception as e:
            print(f"Unexpected error extracting links: {e}")
            break

def paginate_within_thread(driver):
    """Handle pagination within a thread."""
    visited_pages = set()

    while True:
        try:
            current_url = driver.current_url
            if current_url in visited_pages:
                print("Duplicate page detected, stopping pagination.")
                break
            visited_pages.add(current_url)

            extract_external_links_from_thread(driver)

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.pageNav-jump.pageNav-jump--next'))
                )
                next_button.click()
                time.sleep(random.uniform(1, 3))
            except (TimeoutException, NoSuchElementException):
                print("No more pages in thread or 'Next' button not found.")
                break
            except Exception as e:
                print(f"Unexpected error during pagination: {e}")
                break

        except Exception as e:
            print(f"Unexpected error during pagination: {e}")
            break

def close_popup(driver):
    """Close popup if present."""
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'your-popup-close-button-selector'))
        )
        close_button.click()
        print("Popup closed.")
    except TimeoutException:
        print("No popup found or timeout.")
    except NoSuchElementException:
        print("Popup close button not found.")
    except Exception as e:
        print(f"Error closing popup: {e}")

def process_threads(driver, thread_links):
    """Process each thread and extract links."""
    for thread_url in thread_links:
        try:
            print(f"Processing thread: {thread_url}")
            driver.get(thread_url)
            time.sleep(random.uniform(1, 3))
            close_popup(driver)

            extract_external_links_from_thread(driver)
            paginate_within_thread(driver)

        except Exception as e:
            print(f"Error processing thread {thread_url}: {e}")

def main():
    if not os.path.exists('external_links.txt'):
        open('external_links.txt', 'w').close()

    try:
        driver.get(forum_url)

        thread_links = get_thread_links(driver)
        print(f"Found threads: {len(thread_links)}")

        if thread_links:
            process_threads(driver, thread_links)
        else:
            print("No thread links found to process.")

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()