from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class Bot:

    def ReadMessage(self, WebDriver):

        ClassGlobalMessageBox = '_1Ilru'
        
        while True:
            
            try:
                Messages = WebDriver.find_elements_by_class_name(ClassGlobalMessageBox)
                
                if Messages:
                    LastMessage = Messages.pop().text.split('\n')
                    if(LastMessage[0] == '/message'):
                        
                        self.SendMessage(WebDriver, '\033[92mResponse to command')
                        
                        print("Command responde successfully")
                        sleep(1.5)
                        
                    # Testing (Delete)
                    else:
                        print('Reading Message (Not Command)')
                        sleep(0.8)
                        
                else:
                    print('Reading Message (Empty)')
                    sleep(0.8)
                    pass
                
            except TimeoutException:
                print("Timeout")
                pass
            except NoSuchElementException:
                print("Element not found")
                pass
            
    def SendMessage(self, WebDriver, msg):
        
        ClassButton_Send = "_4sWnG"
        
        # msg_box = WebDriver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]')  # /html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]
        
        msg_box = WebDriverWait(WebDriver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]')))
        msg_box.send_keys(msg)
        
        sleep(0.5)
        # msg_box.send_keys(Keys.ENTER)
        # sleep(0.7)
        
        button = WebDriverWait(WebDriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, ClassButton_Send)))
        # # Dice que no lo encuentra porque efectivamente no puso ningun mensaje
        button = WebDriver.find_element_by_class_name(ClassButton_Send)
        button.click()
        # sleep(0.7)