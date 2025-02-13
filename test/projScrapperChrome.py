import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import json
from urllib.parse import urljoin, urlparse

# Path to Chrome WebDriver (update this to your actual path)
chromedriver_path = r"C:\Users\Mu.rpy\projectmeraki\src\scripts\chromedriver.exe"

# Directory to save scraped files
save_directory = "src/data/scraped"


def setup_driver():
    """Sets up the Chrome driver with logging enabled."""
    # Initialize Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Runs in headless mode (remove if you want to see the browser)
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    # Set logging preferences
    caps = options.to_capabilities()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}  # Enables Network logs

    # Initialize the Chrome driver with the specified options and capabilities
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, desired_capabilities=caps)
    return driver

def create_save_directory():
    """Creates the directory to save scraped files."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

def save_file(content, filename):
    """Saves content to a file in the save directory."""
    filepath = os.path.join(save_directory, filename)
    with open(filepath, 'wb') as file:
        file.write(content)

def download_file(url):
    """Downloads a file and saves it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Extract the filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:  # If the URL ends with a slash
            filename = parsed_url.netloc
        save_file(response.content, filename)
        print(f"Saved: {filename}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

def get_page_source(driver, url):
    """Extracts the HTML source code of the page."""
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    html_source = driver.page_source
    save_file(html_source.encode('utf-8'), 'page.html')
    return html_source

def get_static_files(driver):
    """Extracts JS & CSS file URLs from the page."""
    js_css_files = set()
    elements = driver.find_elements(By.XPATH, "//script[@src] | //link[@rel='stylesheet']")
    for elem in elements:
        src = elem.get_attribute("src") or elem.get_attribute("href")
        if src:
            js_css_files.add(src)
    return list(js_css_files)

def get_network_requests(driver):
    """Extracts network request logs."""
    logs = driver.get_log("performance")
    network_data = []
    
    for entry in logs:
        log_entry = json.loads(entry["message"])
        message = log_entry["message"]
        if message["method"] == "Network.requestWillBeSent":
            request = message["params"]["request"]
            network_data.append({
                "url": request["url"],
                "method": request.get("method", "GET"),
                "headers": request.get("headers", {}),
            })
    
    return network_data

def scrape_website(url):
    """Main function to scrape website details."""
    driver = setup_driver()
    create_save_directory()

    print(f"Scraping: {url}")
    
    # Get page source
    get_page_source(driver, url)

    # Get static files (JS & CSS)
    static_files = get_static_files(driver)
    for file_url in static_files:
        # Resolve relative URLs
        full_url = urljoin(url, file_url)
        download_file(full_url)

    # Get network requests
    network_data = get_network_requests(driver)
    with open(os.path.join(save_directory, "network_requests.json"), "w", encoding="utf-8") as f:
        json.dump(network_data, f, indent=4, ensure_ascii=False)
    
    driver.quit()

    print("Scraping complete. Files saved in 'src/data/scraped/'.")

# Example usage
if __name__ == "__main__":
    target_url = "https://example.com"  # Replace with your target site
    scrape_website(target_url)
