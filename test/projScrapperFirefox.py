import os
import requests
import re
import time
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup

def get_page_source(url) -> tuple:
    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options.binary_location = firefox_binary_path
    firefox_driver_path = r"C:\Users\Mu.rpy\projectmeraki\src\scripts\geckodriver.exe"
    service = FirefoxService(executable_path=firefox_driver_path)
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    network_logs = driver.execute_script("return window.performance.getEntries()")
    driver.quit()
    
    return page_source, network_logs

def extract_urls(page_source, network_logs, base_url) -> set:
    soup = BeautifulSoup(page_source, "html.parser")
    sources = set()
    for tag in soup.find_all(["script", "link", "img", "video", "audio", "iframe", "source"]):
        src = tag.get("src") or tag.get("href")
        if src:
            sources.add(urljoin(base_url, src))
    for log in network_logs:
        if "name" in log:
            sources.add(urljoin(base_url, log["name"]))
    return sources

def download_files(sources, folder):
    os.makedirs(folder, exist_ok=True)
    for src in sources:
        try:
            response = requests.get(src, stream=True)
            if response.status_code == 200:
                filename = os.path.join(folder, os.path.basename(urlparse(src).path))
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except:
            pass

def isValidUrl(url) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

def main():
    while True:
        url = input("URL: ")
        if isValidUrl(url):
            page_source, network_logs = get_page_source(url)
            sources = extract_urls(page_source, network_logs, url)
            download_files(sources, "Website Source Codes")
            break

        else:
            print("ERROR 404: URL Not found!")

if __name__ == "__main__":
    main()