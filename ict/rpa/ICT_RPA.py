# -*- coding: utf-8 -*-
"""
Standard RPA step
"""
from pywinauto.application import Application  # RPA
import win32clipboard as wc
import win32con
import time
import pyperclip


# pywinauto second encapsulation
class ICTPywin(object):
    SLEEP_TIME = 0.5
    MAXIMUM_TRY_AGAIN = 3

    # initial an app object
    def __init__(self, app):
        self.app = app
        self.step_info = []
        self.fail_count = 0

    def next_fail(self):  # to find next fail component
        try:
            self.app.type_keys('^F{ENTER}{TAB}{ENTER}')
        except:
            print("\n")
            print("找不到視窗...調參結束")

    def next_step(self):  # to find next component
        try:
            self.app.type_keys('{VK_DOWN}')
        except:
            print("\n")
            print("找不到視窗...調參結束")

    def find_step_info(self):
        self.app.type_keys('^W{TAB 6}^C')
        time.sleep(self.SLEEP_TIME)
        wc.OpenClipboard()
        try:
            Hi_pin = wc.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
            Hi_pin = wc.GetClipboardData(win32con.CF_TEXT)
        wc.CloseClipboard()

        self.app.type_keys('{TAB}^C')
        time.sleep(self.SLEEP_TIME)
        wc.OpenClipboard()
        Lo_pin = wc.GetClipboardData(win32con.CF_UNICODETEXT)
        wc.CloseClipboard()

        self.app.type_keys('{TAB 34}^C')
        time.sleep(self.SLEEP_TIME)
        wc.OpenClipboard()
        Part_N = wc.GetClipboardData(win32con.CF_UNICODETEXT)
        wc.CloseClipboard()

        if self.fail_count > self.MAXIMUM_TRY_AGAIN:
            self.fail_count = 0
            end_flag = -100
            return end_flag
        else:
            if Part_N.isdigit():                                    # 判斷值是否合法
                print("Something wrong, I have to try again...")
                self.fail_count += 1
                return self.find_step_info()
            else:
                if Hi_pin.isdigit() & Lo_pin.isdigit():
                    self.app.type_keys('{TAB 37}{ENTER}')           # 結束
                    self.step_info = [Part_N, Hi_pin, Lo_pin]
                    self.fail_count = 0
                    return self.step_info
                else:
                    print("Something wrong, I have to try again...")
                    self.fail_count += 1
                    return self.find_step_info()

    def input_parameter(self, parameter, test_type, init_mode):
        # input parameter
        '''
        self.app.type_keys('^W')
        self.app.type_keys('{TAB 6}') # HiP
        self.app.type_keys(str(parameter[0])) # HiP

        self.app.type_keys('{TAB}')   # LoP
        self.app.type_keys(str(parameter[1])) # LoP

        self.app.type_keys('{TAB}')   # G1
        self.app.type_keys(str(parameter[2])) # G1

        self.app.type_keys('{TAB}')   # G2
        self.app.type_keys(str(parameter[3])) # G2

        self.app.type_keys('{TAB}')   # G3
        self.app.type_keys(str(parameter[4])) # G3

        self.app.type_keys('{TAB}')   # G4
        self.app.type_keys(str(parameter[5])) # G4

        self.app.type_keys('{TAB}')   # G5
        self.app.type_keys(str(parameter[6])) # G5

        self.app.type_keys('{TAB 9}')   # DLY
        self.app.type_keys(str(parameter[7])) #DLY

        self.app.type_keys('{TAB 2}')   # MODE
        target_mode = str(parameter[8])
        self.__type_mode_test(test_type, target_mode, init_mode)

        self.app.type_keys('{TAB}')     # Avg
        self.app.type_keys(str(parameter[9])) # Avg

        self.app.type_keys('{TAB 2}')   # Rpt
        self.app.type_keys(str(parameter[10])) # Rpt

        self.app.type_keys('{TAB}')   # OFFSET
        self.app.type_keys(str(parameter[11])) # OFFSET

        self.app.type_keys('{TAB 7}{ENTER}') # test

        self.app.type_keys('{TAB 3}{ENTER}') # end
        '''
        self.app.type_keys('{VK_LEFT 22}')

        self.app.type_keys('{VK_RIGHT 3}')
        self.app.type_keys('00')  # OFFSET reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[11]))  # OFFSET
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT 3}')
        self.app.type_keys('00')  # mode reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[8]))  # MODE
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT 3}')
        self.app.type_keys('0000')  # HiP reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[0]))  # HiP
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys('0000')  # LoP reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[1]))  # HiP
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT 2}')
        self.app.type_keys('000')  # DLY reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[7]))  # DLY
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys('^G')  # all G reset
        self.app.type_keys(str(parameter[2]))  # G1
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys(str(parameter[3]))  # G2
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys(str(parameter[4]))  # G3
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys(str(parameter[5]))  # G4
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys(str(parameter[6]))  # G5
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT 2}')
        self.app.type_keys('00')  # AVG reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[9]))  # AVG
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT 1}')
        self.app.type_keys('00')  # Rpt reset
        self.app.type_keys('{ENTER}')
        self.app.type_keys(str(parameter[10]))  # Rpt
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{F8}')  # test

        time.sleep(3*self.SLEEP_TIME)

    def Low_V_change(self):
        self.app.type_keys('{VK_LEFT 22}')
        self.app.type_keys('{VK_RIGHT 2}')
        self.app.type_keys("000000000")  # 歸0
        self.app.type_keys('{ENTER}')
        self.app.type_keys("10")  # 10fF
        self.app.type_keys('{ENTER}')

    def save_MeasV(self, program):
        self.app.type_keys('%FP')
        self.app.type_keys('{TAB 7}{ENTER}')
        self.app.type_keys('{TAB 2}')
        self.app.type_keys("C:\\IAI_AI"+"\\"+program+"\\IAI_m.txt")
        self.app.type_keys('{TAB}{ENTER}')
        time.sleep(3*self.SLEEP_TIME)

    def one_test(self):
        self.app.type_keys('{F8}')
        '''
        self.app.type_keys('^W')
        self.app.type_keys('{TAB 43}{ENTER}')
        self.app.type_keys('{TAB 3}{ENTER}')
        '''
        time.sleep(2*self.SLEEP_TIME)

    def tolerance_input(self, up_limit, low_limit):
        self.app.type_keys('{VK_LEFT 22}')

        self.app.type_keys('{VK_RIGHT 4}')
        self.app.type_keys('0000')
        self.app.type_keys('{ENTER}')
        self.app.type_keys('{}.'.format(up_limit))
        self.app.type_keys('{ENTER}')

        self.app.type_keys('{VK_RIGHT}')
        self.app.type_keys('0000')
        self.app.type_keys('{ENTER}')
        self.app.type_keys('{}.'.format(low_limit))
        self.app.type_keys('{ENTER}')

        '''
        self.app.type_keys('^W')
        self.app.type_keys('{TAB 17}')
        self.app.type_keys('{}'.format(up_limit))
        self.app.type_keys('{TAB 2}')
        self.app.type_keys('{}'.format(low_limit))
        self.app.type_keys('{TAB 15}{ENTER}')
        self.app.type_keys('{TAB 3}{ENTER}')
        '''

    def read_tolerance(self):
        self.app.type_keys('^W')
        self.app.type_keys('{TAB 17}^C')
        time.sleep(self.SLEEP_TIME)
        wc.OpenClipboard()
        plusLm = wc.GetClipboardData(win32con.CF_UNICODETEXT)
        wc.CloseClipboard()
        self.app.type_keys('{TAB 2}^C')
        time.sleep(self.SLEEP_TIME)
        wc.OpenClipboard()
        minusLm = wc.GetClipboardData(win32con.CF_UNICODETEXT)
        wc.CloseClipboard()
        self.app.type_keys('{TAB 18}{ENTER}')
        return plusLm, minusLm
