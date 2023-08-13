import SRC.Log as Log
from os import getcwd
from pathlib import Path
from selenium import webdriver


class Browser():

    NameBrowser = None

    Log = Log.Generate()

    PathSession = getcwd() + '/Data/Session/'
    prefs = {
        "download.default_directory": str(Path(getcwd() + '/Data/WhatsApp/Downloads/')),
        "directory_upgrade": True
    }

    def SetBrowser(self, Name):

        self.NameBrowser = Name

        if Name == 'chrome':
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service

            _BrowserOptions = Options()
            self.SetOptionsForWebDriver(_BrowserOptions)

            WebDriver = webdriver.Chrome(options=_BrowserOptions, service=Service(ChromeDriverManager().install()))

        elif Name == 'firefox':
            from webdriver_manager.firefox import GeckoDriverManager
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service

            _BrowserOptions = Options()
            self.SetOptionsForWebDriver(_BrowserOptions)

            WebDriver = webdriver.Firefox(options=_BrowserOptions, service=Service(GeckoDriverManager().install()))

        elif Name == 'edge':
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            from selenium.webdriver.edge.options import Options
            from selenium.webdriver.edge.service import Service

            _BrowserOptions = Options()
            self.SetOptionsForWebDriver(_BrowserOptions)

            WebDriver = webdriver.Edge(options=_BrowserOptions, service=Service(EdgeChromiumDriverManager().install()))

        return WebDriver



    def SetOptionsForWebDriver(self, _BrowserOptions):

        try:

            _BrowserOptions.add_argument('--user-data-dir=' + self.PathSession)
            _BrowserOptions.add_argument('--disable-extensions')
            _BrowserOptions.add_argument('--disable-dev-shm-usage')
            _BrowserOptions.add_argument('--no-sandbox')
            _BrowserOptions.add_argument('--window-size=1920x1080')
            _BrowserOptions.add_argument('--start-maximized')
            _BrowserOptions.add_argument('--headless')
            _BrowserOptions.add_argument('''--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 
                                            (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
                                         ''')

            _BrowserOptions.add_experimental_option("prefs", self.prefs)

        except AttributeError as e:
            self.Log.Write(f"SetBrowser.py | AttributeError - {self.NameBrowser} # " + str(e))
        except Exception as e:
            self.Log.Write("SetBrowser.py | GenericErr # " + str(e))