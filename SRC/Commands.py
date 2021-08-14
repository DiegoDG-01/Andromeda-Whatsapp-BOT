from re import match
from os import getcwd
from json import load

class CommandManager():
    
    def __init__(self):
        
        self.commandInfo = None
        self.Path = getcwd() + '/Data/Config/Codes.json'
    
    def Read(self, command):
        
        IsCommand = self.__IsCommand(command)
        
        if IsCommand == True:
            
            IsValid, reason = self.__IsValidCommand(command)
            
            if(IsValid == True):
                if(reason == None):
                    return True, None
                else:
                    return True, reason
            else:
                return False, reason  
        else:
            return False, None
    
    def Response(self):
        return self.commandInfo
        
    def execute(self):
        print("Exexute")
        
        
    def __IsCommand(self, command):
        
        regex = "^/[a-zA-Z]+$"
        
        isCommand = match(regex, command)
        
        if isCommand != None:
            return True
        else:
            return False
        
    
    def __IsValidCommand(self, command):
        
        with open(self.Path, 'r') as File:

            commands = load(File)
            
            if(command in commands['Active']):
                self.commandInfo = commands['Active'][command]
                return True, None
            elif(command in commands['Development']):
                self.commandInfo = commands['Development'][command]
                return True, "Command in development"
            else:
                return False, 'Invalid command'
            
    def help():
        print("help")