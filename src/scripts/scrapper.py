import os, json, urllib.parse, requests, shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.scripts.logger import logHandler

def scrape_url(url: str, logger: logHandler) -> Path:
    webDir: Path = Path(f"src/data/websites/{url.replace('://', '.')}")
    scrappedDir: str = webDir / "scrapped"
    if os.path.isdir(webDir):
        shutil.rmtree(webDir)
        logger.warning("You've already scanned this website!")
        logger.debug("Removing previous webdata")
    os.makedirs(f"src/data/websites/{url.replace('://', '.')}")

    if not os.path.exists(scrappedDir):
        os.makedirs(scrappedDir)

    chrome_options = Options()
    chrome_options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True})
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver_path = r"src\scripts\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    page_source_path = os.path.join(scrappedDir, "page_source.html")
    with open(page_source_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    logs = driver.get_log("performance")
    network_logs = []
    downloaded_urls = set()

    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
        except Exception as e:
            continue

        if message.get("method") == "Network.responseReceived":
            response = message.get("params", {}).get("response", {})
            status = response.get("status")
            resource_url = response.get("url")
            if status == 200 and resource_url:
                network_logs.append(message)
                parsed_url = urllib.parse.urlparse(resource_url)
                path = parsed_url.path
                ext = os.path.splitext(path)[1].lower()
                if ext in [".html", ".htm", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"]:
                    if resource_url not in downloaded_urls:
                        downloaded_urls.add(resource_url)
                        try:
                            r = requests.get(resource_url, timeout=10)
                            if r.status_code == 200:
                                filename = os.path.basename(path)
                                if not filename:
                                    filename = "index.html"
                                file_path = os.path.join(scrappedDir, filename)
                                with open(file_path, "wb") as file_out:
                                    file_out.write(r.content)
                        except Exception as e:
                            print(f"Error downloading {resource_url}: {e}")
    misc_log_path = os.path.join(scrappedDir, "misc.json")
    with open(misc_log_path, "w", encoding="utf-8") as f:
        json.dump(network_logs, f, indent=2)

    driver.quit()
    return webDir