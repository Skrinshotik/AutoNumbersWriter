import time
import numpy as np
import pyscreenshot as ImageGrab
import cv2
import os
import pytesseract
import pyautogui
import imutils
# 1850  750
# 1900  790
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Ust Laptop\\Desktop\\Script\\Tesseract\\tesseract.exe'
filename = 'Image.png'
file_resolt = 'C:\\Users\\Ust Laptop\\Desktop\\Script\\RP_Script\\resolts.txt'

run = True
while(run):
    print('#####  MENU  #####')
    print('1.Калибровка зоны отслеживания')
    print('2.Путь к тессеракту')
    print('3.Путь к файлу хранения')
    print('4.Начало работы')
    print('5.Выход')
    u_input = input();

    if(int(u_input)==1):
        print('Через 4 сек будет установленна левая верхняя граница')
        time.sleep(4)
        first_point = pyautogui.position()
        print(first_point)
        print('Через 4 сек будет установленна правая нижняя граница')
        time.sleep(4)
        second_point = pyautogui.position()
        print(second_point)

    if(int(u_input) == 2):
        print('Введите путь к файлу tesseract.exe (обязательно с двойными слешами \\)')
        u_input = input()
        pytesseract.pytesseract.tesseract_cmd = u_input

    if(int(u_input) == 3):
        print('Введите путь к файлу с расширением .txt (обязательно с двойными слешами \\)')
        file_resolt = input()

    if(int(u_input) == 4):
        while(True):
            x = 1
            text = ''
            while(True):
                screen = np.array(ImageGrab.grab(bbox=(first_point.x,first_point.y,second_point.x,second_point.y)))
                cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
                cv2.imwrite(filename,screen)
                x = x+1
                if(x == 2):
                    cv2.destroyAllWindows()
                    break

            img = cv2.imread('Image.png')

            img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

            #thresh = cv2.GaussianBlur(sharpen, (3,3), 0)

            #sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            #sharpen = cv2.filter2D(thresh, -1, sharpen_kernel)

            thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


            text = pytesseract.image_to_string(thresh, lang='eng', config='outputbase digits')


            cv2.imwrite(filename,thresh)

            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            #thresh = cv2.GaussianBlur(thresh, (3,3), 0)
            #text = pytesseract.image_to_string(thresh, config='--psm 11 digits')

            #text = pytesseract.image_to_string(img)               30
            output = open(file_resolt,'a+')
            if(text == ''):
                print('ERROR')
            else:
                print('Распознано -->', text)
                try:
                    output.write('{}, '.format(int(text)))
                except:
                    output.write('{}, '.format(text))
            output.close()
            time.sleep(1)

    if(int(u_input) == 5):
        print('Завершение работы')
        break
