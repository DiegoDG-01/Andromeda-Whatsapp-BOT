#######################################
#  __        _____ _   _ ____ _____   #
#  \ \      / /_ _| \ | / ___|_   _|  #
#   \ \ /\ / / | ||  \| \___ \ | |    #
#    \ V  V /  | || |\  |___) || |    #
#     \_/\_/  |___|_| \_|____/ |_|    #
#                                     #
#    Basic Installer for Windows OS   #
#                                     #
#######################################

import os
import sys
import shutil
import platform
import subprocess
import pkg_resources
from os import getcwd
from pathlib import WindowsPath
from json import load, dump

def __ColorsInit():
    # Codes for colors in the
    return {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m'
    }

def __get_paths(Type):
    Paths = {
        'home': getcwd(),
        'requirements': getcwd() + '/requirements.txt',
        'SRC': getcwd() + '/SRC/'
    }

    return Paths[Type]

def __validations(Colors = __ColorsInit()):
    if platform.system() != 'Windows':
        print('This script is only for Windows')
        exit()

    if not os.path.exists(__get_paths('requirements')):
        print('Requirements file not found')
        exit()

    if not os.path.exists(__get_paths('SRC')):
        print('SRC folder not found')
        exit()

    if sys.version_info[0] < 3:
        print('Python 3 is required')
        exit()

    if pkg_resources.get_distribution('pip').version < '19.0.0':
        print(Colors['red'] + 'Pip version is not compatible, please update it' + Colors['end'])
        exit()

    if pkg_resources.get_distribution('virtualenv').version < '20.13.0':
        print(Colors['red'] + 'Virtualenv 20.13.0 or higher is required' + Colors['end'])


# Install virtualenv in windows in the current folder
def __install_virtualenv(Colors = __ColorsInit()):

    print('----------------------------------------')
    print('Installing virtualenv...')
    print('----------------------------------------')
    subprocess.call(['python3', '-m', 'venv', __get_paths('home') + '\\venv'])
    print('Virtualenv installed\n')

    # Activate virtualenv
    print('----------------------------------------')
    print('Activating virtualenv...')
    print('----------------------------------------')
    subprocess.call([__get_paths('home') + '\\venv\\Scripts\\activate.bat'])
    print(Colors['green'] + 'Virtualenv activated\n' + Colors['end'])

def __install_requirements(Colors = __ColorsInit()):
    print('----------------------------------------')
    print('Installing requirements...')
    print('----------------------------------------')
    # Send the output to null
    subprocess.call(['pip3', 'install', '-r', __get_paths('requirements')], stdout=subprocess.DEVNULL)
    print(Colors['green'] + 'Requirements installed\n' + Colors['end'])

    # Verify if the requirements are installed from requirements.txt
    try:
        print('----------------------------------------')
        print('Verifying requirements...')
        print('----------------------------------------')
        with open(__get_paths('requirements'), 'r') as f:
            requirements = f.read().splitlines()
            for requirement in requirements:
                pkg_resources.require(requirement)
                print(requirement + ' is installed')

        print(Colors['green'] + 'All requirements are installed' + Colors['end'])
    except pkg_resources.DistributionNotFound as e:
        print(Colors['red'] + 'Requirements not installed' + Colors['end'])
        exit()


def __configure():

    PathSRC = __get_paths('SRC')
    PathLang = str(WindowsPath(PathSRC + '\\Data\\Config\\Lang\\'))
    PathConfig =str(WindowsPath(PathSRC + '\\Data\\Config\\'))

    # Set the language
    print('----------------------------------------')
    print('Setting the language...')
    print('----------------------------------------')

    print('Available languages:')
    print('1. English')
    print('2. Spanish')

    while True:
        try:
            Language = int(input('Select the language: '))
            if Language == 1:
                Language = 'English'
                break
            elif Language == 2:
                Language = 'Spanish'
                break
            else:
                print('Invalid language')
        except ValueError:
            print('Invalid language')

    if os.path.exists(PathLang + '\\' + Language + '\Codes.json'):
        shutil.copy(PathLang + '\\' + Language + '\Codes.json', PathConfig)
    else:
        print('Language not found')
        exit()

    if os.path.exists(PathLang + '\\' + Language + '\Config.json'):
        shutil.copy(PathLang + '\\' + Language + '\Config.json', PathConfig)
    else:
        print('Config not found')
        exit()
    

    print('----------------------------------------')
    print('Language set to ' + Language)
    print('----------------------------------------\n')

    print('----------------------------------------')
    print('Setting to listening chat...')
    print('----------------------------------------')

    with open(PathConfig + '\Config.json', 'r+') as file:
        Config = load(file)

        chatname = input('Write the name chat used to listening Bot: ')

        Config['main']['Default']['WhatsappName'] = chatname

        file.seek(0)
        dump(Config, file, indent=4)
        file.truncate()

        


def main():
    __validations()
    __install_virtualenv()
    __install_requirements()
    __configure()

if __name__ == '__main__':
    main()