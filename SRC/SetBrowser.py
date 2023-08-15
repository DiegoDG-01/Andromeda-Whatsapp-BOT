import Log
from os import getcwd
from pathlib import Path


class Browser():

    NameBrowser = None

    Log = Log.Generate()

    PathSession = getcwd() + '/Data/Session/'
    prefs = {
        "download.default_directory": str(Path(getcwd() + '/Data/WhatsApp/Downloads/')),
        "directory_upgrade": True
    }

    def SetBrowser(self, Name):

        try:

            self.NameBrowser = Name

            if Name == 'chrome':
                from webdriver_manager.chrome import ChromeDriverManager as BrowserManager
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver import chrome as webdriver

            elif Name == 'firefox':
                from webdriver_manager.firefox import GeckoDriverManager as BrowserManager
                from selenium.webdriver.firefox.options import Options
                from selenium.webdriver.firefox.service import Service
                from selenium.webdriver import firefox as webdriver

            elif Name == 'edge':
                from webdriver_manager.microsoft import EdgeChromiumDriverManager as BrowserManager
                from selenium.webdriver.edge.options import Options
                from selenium.webdriver.edge.service import Service
                from selenium.webdriver import edge as webdriver
                
            else:
                self.Log.Write("SetBrowser.py | BrowserErr | SetBrowser # Browser not found")
                return False

            _BrowserOptions = Options()
            self.SetOptionsForWebDriver(_BrowserOptions)

            WebDriver = webdriver(options=_BrowserOptions, service=Service(BrowserManager().install()))

            return WebDriver

        except Exception as e:
            self.Log.Write("SetBrowser.py | GenericErr | SetBrowser # " + str(e))
            return False


    def SetOptionsForWebDriver(self, _BrowserOptions):

        try:

            # Global options
            # _BrowserOptions.add_argument('--headless')

            if self.NameBrowser == 'chrome' or self.NameBrowser == 'edge':

                _BrowserOptions.add_argument('--user-data-dir=' + self.PathSession)
                _BrowserOptions.add_argument('--disable-extensions')
                _BrowserOptions.add_argument('--disable-dev-shm-usage')
                _BrowserOptions.add_argument('--no-sandbox')
                _BrowserOptions.add_argument('--window-size=1920x1080')
                _BrowserOptions.add_argument('--start-maximized')
                _BrowserOptions.add_argument('''--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 
                                                (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
                                             ''')

                _BrowserOptions.add_experimental_option("prefs", self.prefs)

        except AttributeError as e:
            self.Log.Write(f"SetBrowser.py | AttributeError - {self.NameBrowser} # " + str(e))
        except Exception as e:
            self.Log.Write("SetBrowser.py | GenericErr # " + str(e))