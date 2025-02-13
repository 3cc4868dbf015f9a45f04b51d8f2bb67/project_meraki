import json
import time
from selenium import webdriver
from selenium.webdriver.opera.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# **** Configuration ****
# Update these paths to match your system
opera_gx_binary = r"C:\Users\justd\AppData\Local\Programs\Opera GX\opera.exe"       # e.g., "C:\\Users\\YourName\\AppData\\Local\\Programs\\Opera GX\\launcher.exe"
operadriver_path = r"C:\Path\To\operadriver.exe"             # e.g., "C:\\Path\\To\\operadriver.exe"

# Target URL to scrape
target_url = "https://example.com"  # Change this to your desired website

# **** Set up OperaGX options ****
options = Options()
options.binary_location = opera_gx_binary

# Set desired capabilities to enable performance logging (i.e. network logs)
capabilities = DesiredCapabilities.OPERA.copy()
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

# Initialize the Opera WebDriver with the specified binary and capabilities
driver = webdriver.Opera(options=options,
                          executable_path=operadriver_path,
                          desired_capabilities=capabilities)

# Optionally, enable network tracking via Chrome DevTools Protocol (CDP)
# This step is needed to start capturing network events.
driver.execute_cdp_cmd("Network.enable", {})

# Navigate to the target URL
driver.get(target_url)

# Wait a few seconds to allow the page and its network traffic to load
time.sleep(5)

# ----- Scrape "Inspect Element" data -----
# 1. Get the full HTML source (similar to the Elements panel)
html_source = driver.page_source
print("------ PAGE SOURCE ------")
print(html_source)

# 2. Get network performance logs (similar to the Network tab)
print("\n------ NETWORK LOGS ------")
logs = driver.get_log("performance")
for entry in logs:
    try:
        # Each log entry is a JSON string; parse it into a Python dict.
        log_json = json.loads(entry["message"])["message"]
        # Here, we filter to show only events related to network activity.
        if log_json.get("method", "").startswith("Network."):
            print(json.dumps(log_json, indent=2))
    except Exception as e:
        print("Error processing log entry:", e)

# Clean up: close the browser
driver.quit()
