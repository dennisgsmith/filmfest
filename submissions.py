# Python 3.9.0
# submissions.py
__version__ = '0.2.1'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from pathlib import Path
import time
import os
from settings import get_user_creds

# set up path local to project
HERE = Path(__file__).parent
DATA_FOLDER = HERE / 'data'
try: # create path
    Path.mkdir(DATA_FOLDER)
except FileExistsError:
    pass

# initialize chromedriver and ingest its system path
login_url = "https://filmfreeway.com/login"
submissions_url = "https://filmfreeway.com/submissions"
dl_path = str(DATA_FOLDER)


def setup_chrome():
    '''
    configure boilerplate settings for Options()
    return amended Options() object
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless") # comment out this line to see the action
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": f"{DATA_FOLDER}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    return chrome_options


def site_login(browser, login_url, username, password):
    '''
    take in driver, log into account with user creds
    '''
    browser.get(login_url)
    browser.find_element_by_id("user_account_email").send_keys(username)
    browser.find_element_by_id("user_account_password").send_keys(password)
    browser.find_element_by_name("commit").click()


def submissions_download(browser, submissions_url):
    '''
    navigate to submissions page and initate download
    '''
    browser.get(submissions_url) # go to submissions tab url
    browser.find_element_by_xpath('//*[@id="submission-index"]/div[3]/div[5]/div[2]/a[2]').click() # open dropdown
    browser.find_element_by_xpath('//*[@id="dropdown-export-content"]/ul/li[1]/a').click() # select element from dropdown
    WebDriverWait(browser, 1) # wait 1 second for javascript motion-window
    browser.find_element_by_id('export_configuration').click() # export config dropdown
    browser.find_element_by_xpath('//*[@id="export_configuration"]/option[2]').click() # select "Basic Summary"
    browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/form/div[3]/button').click() # click export button


def download_handler(browser, download_dir):
    '''
    take in driver and downlad file to specified directory
    '''
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


def main():
    # ask for user keys and create local env if needed
    USER, PASS = get_user_creds()
    # make sure chromedriver is in system PATH or specify "executable_path" kwarg
    chrome_options = setup_chrome()
    browser = webdriver.Chrome(options=chrome_options) # initiate driver
    site_login(browser, login_url, USER, PASS)
    submissions_download(browser, submissions_url)
    download_handler(browser, dl_path)
    time.sleep(100) # long enough to export all submissions
    browser.quit()


# run the program
if __name__=="__main__":
    main()