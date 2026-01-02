import eel
from sys import exit
from os import getcwd
from os.path import join

def startHTML():
    try:
        print('\n----------------------- STARTING HTML APPLICATION -----------------------')
        BASEDIR = getcwd(); print('Base Directory:\t\t', BASEDIR)
        WEBDIR = join(BASEDIR,'06_Main_Code', 'frontend'); print('Web Dir:\t\t',WEBDIR,'\n')
        eel.init(WEBDIR); eel.start("index.html", mode="Chrome")
    except Exception as e: exit()
