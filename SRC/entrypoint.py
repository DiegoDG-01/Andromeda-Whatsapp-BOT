import Bot
import Config
from sys import argv
from os import getcwd
from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


def InitWebDriver():
    
    URL = 'https://web.whatsapp.com/'
    
    PathSession = getcwd() + '/Data/Session/'
    
    _Chrome_options = Options()
    _Chrome_options.add_argument('--user-data-dir='+PathSession)
    _Chrome_options.add_argument('--disable-extensions')
    _Chrome_options.add_argument('--disable-dev-shm-usage')
    _Chrome_options.add_argument('--no-sandbox')
    
    # Iniciar sin mostrar la ventana del navegador
    # _Chrome_options.add_argument('headless')
     
    try:
        WebDriver = Chrome(options = _Chrome_options)   

        WebDriver.maximize_window()
        WebDriver.get(URL)
        
        return WebDriver
    except:
        WebDriver.quit()
        print('Error')

if(__name__ == '__main__'):
    
    try:
    
        WebDriver = InitWebDriver()
        
        Bot = Bot.Bot()
        Config = Config.Config(WebDriver)
        
        
        Bot.ReadMessage(WebDriver)
        
        WebDriver.quit()
    except KeyboardInterrupt:
        print('\nInterrupted By Keyboard')
        WebDriver.quit()
        

# URL = 'https://web.whatsapp.com/'
# PathSession = getcwd()

# ClassSearchBar = "_13NKt"
# ClassButton_Search = "_28-cz"
# ClassButton_Send = "_4sWnG"

# with Chrome(options=_Chrome_options) as WebDriver:

#     WebDriver.maximize_window()
#     WebDriver.get(URL)
    
#     name = "Testing BOT"
#     msg = "TEST (FOR) #4"
    
#     user = WebDriverWait(WebDriver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@title = "Testing BOT"]')))
#     # user = WebDriver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
#     user.click()
    
#     msg_box = WebDriverWait(WebDriver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]')))
    
#     for i in range(5):

#         # msg_box = WebDriver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]')  # /html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]
        
#         # WebDriverWait(WebDriver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]')))
#         msg_box.send_keys(msg)
#         sleep(0.5)
#         msg_box.send_keys(Keys.ENTER)
#         # sleep(0.7)
        
#         # button = WebDriverWait(WebDriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, ClassButton_Send)))
#         # # Dice que no lo encuentra porque efectivamente no puso ningun mensaje
#         # # button = WebDriver.find_element_by_class_name(ClassButton_Send)
#         # button.click()
#         # sleep(0.7)
        
#         sleep(1)
        
#         print("Mensaje enviado!")
