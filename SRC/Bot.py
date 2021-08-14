##############################################
##       __      _____  ___        __       ##
##      /""\    (\"   \|"  \      /""\      ##
##     /    \   |.\\   \    |    /    \     ##
##    /' /\  \  |: \.   \\  |   /' /\  \    ##
##   //  __'  \ |.  \    \. |  //  __'  \   ##
##  /   /  \\  \|    \    \ | /   /  \\  \  ##
## (___/    \___)\___|\____\)(___/    \___) ##
##                                          ##
##         It's a palindrome name <3        ##  
##                                          ##
##############################################     

import Commands
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class Bot:
    
    def __init__(self):
        self.ComandManager = Commands.CommandManager()
        
    def Welcome(self, WebDriver):
        self.WriteMessage(WebDriver, "Welcome, I'm {undifine}")
        self.SendMessage(WebDriver)

    def ReadMessage(self, WebDriver):
        
        # self.Welcome(WebDriver)

        ClassGlobalMessageBox = '_1Ilru'
        
        while True:
            
            try:
                Messages = WebDriver.find_elements_by_class_name(ClassGlobalMessageBox)
                
                if Messages:
                    
                    Message = Messages.pop().text.split('\n')
                    
                    Command = self.ComandManager.Read(Message[0])
                    
                    if(Command[0] == True and Command[1] is None):  
                        
                        commandInfo = self.ComandManager.Response()                  
                        
                        self.WriteMessage(WebDriver, commandInfo)
                        self.SendMessage(WebDriver)
                            
                        print("Command responde successfully")
                        sleep(3)
                    
                    elif(Command[0] == True and Command[1] is not None):
                        
                        # self.SendMessage(WebDriver, 'TEST'+ Keys.SHIFT + Keys.ENTER +'TEST')
                        self.WriteMessage(WebDriver, Command[1])
                        self.SendMessage(WebDriver)
                        
                        print("Command responde successfully")
                        sleep(3)
                        
                    # Testing (Delete)
                    else:
                        sleep(2)
                        
                else:
                    print('Reading Message (Empty)')
                    sleep(2)
                    pass
                
            except TimeoutException:
                print("Timeout")
                pass
            except NoSuchElementException:
                print("Element not found")
                pass
            
    def SendMessage(self, WebDriver):
        
        ClassButton_Send = "_4sWnG"
        
        button = WebDriverWait(WebDriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, ClassButton_Send)))

        button = WebDriver.find_element_by_class_name(ClassButton_Send)
        button.click()
        
    def WriteMessage(self, WebDriver, msg):
        
        if(type(msg) == str):
            msg = [msg]
        
        msg_box = WebDriverWait(WebDriver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]')))
        msg_box.click()
        
        for i in msg:
            msg_box.send_keys(i + (Keys.SHIFT + Keys.ENTER))
            sleep(0.20)