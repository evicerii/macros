import time
import mouse
import keyboard
import threading
import configparser
import logging
from datetime import date

from numpy import *

from ctypes import *

#pyinstaller --add-data "config.ini:." main.py

config = configparser.ConfigParser()
config.read('config.ini')

check_click_event = threading.Event()
timer_event = threading.Event()
replay_event = threading.Event()
click_event = threading.Event()


lock = threading.Lock()
logging.basicConfig(level=logging.INFO, filename=f'l{date.today()}.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w')
logging.info(f'macros start')

mouse_road=[]
timer_list=[]

click_event.clear()
check_click_event.clear()
timer_event.clear()
replay_event.clear()

def start_rec():
    if check_click_event.is_set():
        ...
    else:
        logging.info(f'start rec')
        print('Запись начата')
        mouse_road.clear()
        check_click_event.set()
        write_mouse_road()
        time.sleep(1)

def press_stop_rec():
    logging.info(f'stop rec')
    if check_click_event.is_set():
        print('Выход')
        check_click_event.clear()

def replay_rec():
    logging.info(f'replay rec')
    print('Воспроизведение')
    if check_click_event.is_set():
        return
    replay_event.set()
    while True:
        time.sleep(1)
        for i in mouse_road:
            if replay_event.is_set():
                mouse.move(i[0][0], i[0][1])
                if i[1] == True:
                    mouse.click()
                time.sleep(0.01)
            else:
                return
            
def press_out():
    logging.info(f'stop macros')
    if replay_event.is_set():
        print('стоп')
    
        # windll.user32.BlockInput(False)
        replay_event.clear()

def write_mouse_road():
    while True:
        if check_click_event.is_set():
            mouse_road.append([mouse.get_position(), click_event.is_set()])
            time.sleep(0.01)
        else:
            return      

def chk_click():
    while True:
        time.sleep(0.05)
        mouse.on_click(record_click)
        
def record_click():
    if check_click_event.is_set():
        click_event.set()
        time.sleep(0.01)
        click_event.clear()
        mouse.unhook_all()

def main_start():  
    while True:
        if keyboard.is_pressed(str(config.get('General','start_record'))[1:-1]):
            start_rec()
        if keyboard.is_pressed(str(config.get('General','replay'))[1:-1]):
            replay_rec()
def main_stop():
    while True:
        if keyboard.is_pressed(str(config.get('General','end_record'))[1:-1]):
            press_stop_rec()
        if keyboard.is_pressed(str(config.get('General','out_record'))[1:-1]):
            press_out()
        time.sleep(0.01)
        
if __name__ == '__main__':
    
    main_start_thread = threading.Thread(target=main_start)
    main_stop_thread = threading.Thread(target=main_stop)
    mouse_click_thread = threading.Thread(target=chk_click, daemon=True)
    # timer_thread = threading.Thread(target=timer, daemon=True)
    
    main_start_thread.start()
    main_stop_thread.start()
    mouse_click_thread.start()
    # timer_thread.start()