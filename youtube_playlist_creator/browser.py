from selenium import webdriver


def init_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=8000")
    options.add_argument("user-data-dir=Default")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options,
                              executable_path='chromedriver.exe')
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.set_window_size(1200, 900)
    driver.implicitly_wait(5)
    return driver

driver = init_chrome()
driver.get("https://youtube.com/login")
input()