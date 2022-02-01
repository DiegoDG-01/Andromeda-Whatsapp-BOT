import os
import subprocess
import time # DELETE THIS AFTER TESTING
import platform
from pathlib import Path

def __ColorsInit():
    # Colors for the terminal
    return {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[97m',
        'end2': '\033[0m'
    }

def __delete_files():
    # Delete the file
    os.remove(__get_paths("main"))
    print(Colors['green'] + '\nThe all files was deleted' + Colors['end'])

def __get_paths(Type):

    MainPath = os.getcwd()

    if(Type == 'requirements'):
        return MainPath+"/requirements.txt"
    elif(Type == 'SRC'):
        return MainPath+"/SRC/"
    elif(Type == 'homeUser'):
        return str(Path.home())

def __install_virtualenv():
    # Install the virtualenv
    print(Colors['green'] + '\n# Installing the virtualenv' + Colors['end'])
    subprocess.run('pip3 install virtualenv==20.13.0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    if subprocess.run("pip3 list | grep 'virtualenv'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL):
        print(Colors['white'] + '>> The virtualenv was installed' + Colors['end'])
        return True
    else:
        print(Colors['red'] + '\nError: The virtualenv was not installed' + Colors['end'])
        return False

def __install_dependencies():

    # Dependencies for the bot
    requirements = __get_paths("requirements")

    if os.path.exists(requirements):
        print(Colors['green'] + '\n# Requirements found' + Colors['end'])

        # Waiting in the terminal instalation of the dependencies
        print(Colors['white'] + '>> Installing the dependencies')
        print(">> Wait in terminal while the dependencies are installed" + Colors['end'])
        time.sleep(2)
        # Check if the dependencies are installed
        # subprocess.run('pip3 install -r ' + requirements, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


        if __check_dependencies():
            return True
        else:
            return False
    else:
        print(Colors['red'] + '\nError: The requirements.txt file does not exist' + Colors['end'])
        return False

def __check_dependencies():

    depNotInstalled = 0

    # Check if the dependencies are installed
    print(Colors['green'] + '\n# Checking the dependencies' + Colors['end'])

    with open('requirements.txt') as requirements:
        for line in requirements:

            # print("pip3 list | grep '"+line.split()[0]+"' | awk '{print $1}' > /dev/null")

            # Check if the package is installed or not
            package = subprocess.run("pip3 list | grep '"+line.split()[0]+"' | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

            if package == '':
                print(Colors['white'] + '>> The package ' + line.strip() + Colors['red'] + ' is not installed' + Colors['end'])
                depNotInstalled += 1
            else:
                print(Colors['white'] + '>> The package ' + line.strip() + Colors['green'] + ' is installed' + Colors['end'])

    if depNotInstalled != 0:
        cont = str.lower(input(Colors['yellow'] + '\n% Not all dependencies are installed, are you continue to installation? (y/n):' + Colors['end']))

        if cont == 'y':
            return True
        else:
            return False


def __install_bot():

    # Install the bot
    pathHome = __get_paths("homeUser")
    pathSRC = __get_paths("SRC");
    pathInstall = __get_paths("install")

    customInstall = input(Colors['yellow'] + '\n% Enter the custom path(enter for default path): ' + Colors['end'])

    if customInstall != '':
        pathInstall = pathHome + '/' + customInstall
    else:
        pathInstall = pathHome+"/WBB/"


    if os.path.exists(pathSRC):
        print(Colors['green'] + '\n# The bot source is found' + Colors['end'])
        print(Colors['white'] + '>> Directory: ' + pathSRC + Colors['end'])

        if not os.path.exists(pathInstall):
            print(Colors['green'] + '\n# Creating the installation directory' + Colors['end'])
            print(Colors['white'] + '>> Directory: ' + pathInstall + Colors['end'])

            os.makedirs(pathInstall)

            if not os.path.exists(pathInstall):
                print(Colors['red'] + '\nError: The directory was not created' + Colors['end'])
                return False

            print(Colors['green'] + '\n# Copying the bot source' + Colors['end'])
            os.system('cp -r ' + pathSRC + ' ' + pathInstall)
            print(Colors['white'] + '>> Copied complete' + Colors['end'])

            return True

    else:
        print(Colors['red'] + '\nError: The bot source does not exist' + Colors['end'])
        return False

def __get_general_info():

    # Only this Package Manager is required
    Managers = {
        'brew': 'brew',
        'apt': 'apt-get'
    }

    # Validating the Package Manager
    for key, value in Managers.items():
        if os.system('which ' + value + '> /dev/null') == 0:
            PM = key
            Check = True
            break
        else:
            PM = "Not available"
            Check = False

    # Create a dictionary with the general info
    Global = {
        'Package Manager': PM,
        "Checked": Check,
        'Operative System': platform.uname()[0],
        'Operative System Version': platform.uname()[2]
    }

    # Return the dictionary with the general info
    return Global

def __welcome(Colors):

    # Show welcome message with a nice ASCII art :)
    message = Colors['green'] + '''
                ██╗  ██╗  █████╗  ██╗       ██████╗ 
                ██║  ██║ ██╔══██╗ ██║      ██╔═══██╗
                ███████║ ███████║ ██║      ██║   ██║
                ██╔══██║ ██╔══██║ ██║      ██║   ██║
                ██║  ██║ ██║  ██║ ███████╗ ╚██████╔╝
                ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚══════╝  ╚═════╝ 
       The next installer for the Linux/Unix Operating System.
    ''' + Colors['end']

    # Show the message
    print(message)

def main(Info, Colors):

    # Show welcome message
    __welcome(Colors)

    # Show general info about the system
    for key, value in Info.items():
        if(key != 'Checked'):
            print(Colors['purple'] + key + ': ' + Colors['end'] + value)

    while (True):
        try:
            # Ask for the Package Manager
            # if is not valid finish the installer
            if Info['Checked'] is True:
                install = str.lower(input(Colors['cyan'] + '''\nYour system is compatible.\nDo you want to install the bot? (y/n): ''' +Colors['end']))

                # If the answer is yes, start the installer
                if install == 'y':
                    if __install_virtualenv():
                        if __install_dependencies():
                            if __install_bot():
                                print(Colors['green'] + '\nThe bot was installed successfully' + Colors['end'])
                            else:
                                print(Colors['red'] + '\nError: The bot was not installed' + Colors['end'])
                            break
                        else:
                            print(Colors['red'] + '\n# Error: The dependencies are not installed' + Colors['end'])
                            break

                # If the answer is no or other character, finish the installer
                else:
                    print(Colors['red'] + '\nExiting...' + Colors['end'])
                    break
            else:
                print(Colors['red'] + '\nYour system is not compatible.\nExiting...' + Colors['end'])
                break

        except KeyboardInterrupt as e:
            print(Colors['red'] + '\n\nError: KeyboardInterrupt canceling the installation' + Colors['end'])
            break



if __name__ == '__main__':

    os.system('clear')

    Colors = __ColorsInit()
    Info = __get_general_info()

    main(Info, Colors)