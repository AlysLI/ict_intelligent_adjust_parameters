# -*- coding: utf-8 -*-
from pywinauto.application import Application  # RPA
import re

from common import ICT_general_function
from ict.rpa import ICT_RPA


def rmodelearning(self):
    # 電阻Tolerance標準
    # 10.1-13 ohm                    (75% , 20%)
    # 13.1-16 ohm                    (60% , 20%)
    # 16.1-20 ohm                    (50% , 20%)
    # 20.1-35 ohm                    (40% , 20%)
    # 35.1-300 ohm                   (30% , 20%)
    # 300.1-10k ohm                  (25% , 20%)
    # 10.001k-100k ohm               (25% , 25%)
    # >100k  ohm                     (30% , 30%)

    step_ExpextV = self.ExpectV
    number_part = re.findall(r"\d+\.?\d*", step_ExpextV)
    number_part = number_part[0]
    if len(number_part) == len(step_ExpextV):
        unit_part = ""
    else:
        unit_part = step_ExpextV[len(number_part):]
    number_part = float(number_part)

    # ###################### Tolerance check #######################
    if unit_part == '' and number_part >= 10 and number_part <= 13:
        up_limit = 75
        low_limit = 20
    elif unit_part == '' and number_part > 13 and number_part <= 16:
        up_limit = 60
        low_limit = 20
    elif unit_part == '' and number_part > 16 and number_part <= 20:
        up_limit = 50
        low_limit = 20
    elif unit_part == '' and number_part > 20 and number_part <= 35:
        up_limit = 40
        low_limit = 20
    elif unit_part == '' and number_part > 35 and number_part <= 300:
        up_limit = 30
        low_limit = 20
    elif [(unit_part == '' and number_part > 300 and number_part <= 1000) or
          (unit_part == 'K' and number_part > 0 and number_part <= 10)]:
        up_limit = 25
        low_limit = 20
    elif unit_part == 'K' and number_part > 10 and number_part <= 100:
        up_limit = 25
        low_limit = 25
    elif unit_part == 'K' and number_part > 100:
        up_limit = 30
        low_limit = 30
    else:
        up_limit = ''
        low_limit = ''

    if up_limit != '':
        plusLm, minusLm = tolerance_read()
        tolerance_adj(up_limit, low_limit, plusLm, minusLm)
    print("Tolerance check is over")

    parameter_test = []
    parameter_ls = [[self.HiP, self.LoP, self.G1, self.G2, self.G3, self.G4,
                     self.G5, self.DLY, self.MODE, self.avge, self.RPT,
                     self.OFFSET]]
    parameter_Q = [0]

    DLY = [0, 50, 100]
    AVG = [0, 1, 2, 4]
    RPT = [1, 2, 4, 5]
    now_quality = 0.1  # can be any number <1

    quality = self.test_parameter(parameter_ls[0])
    if quality >= now_quality:
        now_quality = quality
    if quality == 4:
        return self.data_process.parameter_save(parameter_ls, parameter_Q)

    parameter_test = [self.HiP, self.LoP, 0, 0, 0, 0, 0, 0, self.MODE, 0, 0, 0]
    power_test = False
    if power_test:  # power test
        for delay in DLY:
            last_parametar = parameter_test[7]
            parameter_test[7] = delay
            quality = self.test_parameter(parameter_test)
            if quality >= now_quality:
                now_quality = quality
                parameter_ls.append(parameter_test.copy())
                parameter_Q.append(quality)
            else:
                parameter_test[7] = last_parametar
        self.data_process.parameter_save(parameter_ls, parameter_Q)
        return 0

    # R value adjudge
    if number_part < 20 and unit_part == '':  # R<20 Ohm
        print("over")
        return 0

    # ###################### Hi Lo change #######################
    parameter_test = [self.LoP, self.HiP, 0, 0, 0, 0, 0, 0, self.MODE, 0, 0, 0]
    quality = self.test_parameter(parameter_test)

    if quality >= now_quality:
        now_quality = quality
        parameter_ls.append(parameter_test.copy())
        parameter_Q.append(quality)
    else:
        parameter_test = [self.HiP, self.LoP, 0, 0, 0, 0, 0, 0, self.MODE, 0, 0, 0]
    print("Hi Lo change test is over")

    # ###################### Delay test #######################
    total_len = len(DLY)
    progress = 0
    for delay in DLY:
        if quality == 4:
            return self.data_process.parameter_save(parameter_ls, parameter_Q)
        progress += 1
        message = "processing delay test, delay = {}  ...".format(delay)
        ICT_general_function.processbar(progress, total_len, message)

        last_parametar = parameter_test[7]
        parameter_test[7] = delay
        quality = self.test_parameter(parameter_test)
        if quality >= now_quality:
            now_quality = quality
            parameter_ls.append(parameter_test.copy())
            parameter_Q.append(quality)
        else:
            parameter_test[7] = last_parametar
    print("Delay test is over")

    # ###################### Avg test #######################
    total_len = len(AVG)
    progress = 0
    for avg in AVG:
        if quality == 4:
            return self.data_process.parameter_save(parameter_ls, parameter_Q)
        progress += 1
        message = "processing Avg test, Avg = {}  ...".format(avg)
        ICT_general_function.processbar(progress, total_len, message)

        last_parametar = parameter_test[9]
        parameter_test[9] = avg
        quality = self.test_parameter(parameter_test)
        if quality >= now_quality:
            now_quality = quality
            parameter_ls.append(parameter_test.copy())
            parameter_Q.append(quality)
        else:
            parameter_test[9] = last_parametar
    print("Avg test is over")

    # ###################### mode test #######################
    # 電阻模式
    # 0-300 ohm    MODE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # 300-3K ohm   MODE = [0, 1, 2, 3, 4, 5]
    # 3K-30K ohm   MODE = [0, 1, 2, 3, 4]
    # 30K-500K ohm MODE = [0, 1, 2, 3]
    # 500K-3M ohm  MODE = [0, 1, 2]
    # >3M ohm      MODE = [0, 2]
    if unit_part == '' and number_part <= 300:
        MODE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    elif (unit_part == '' and number_part > 300) or \
         (unit_part == 'K' and number_part <= 3):
        MODE = [0, 1, 2, 3, 4, 5]
    elif unit_part == 'K' and number_part > 3 and number_part <= 30:
        MODE = [0, 1, 2, 3, 4]
    elif unit_part == 'K' and number_part > 30 and number_part <= 500:
        MODE = [0, 1, 2, 3]
    elif (unit_part == 'K' and number_part > 500) or \
         (unit_part == 'M' and number_part <= 3):
        MODE = [0, 1, 2]
    elif unit_part == 'M' and number_part > 3:
        MODE = [0, 2]

    parameter_test[8] = self.MODE
    total_len = len(MODE)
    progress = 0
    for mode in MODE:
        progress += 1
        message = "processing mode test {}...".format(mode)
        ICT_general_function.processbar(progress, total_len, message)

        last_parametar = parameter_test[8]
        parameter_test[8] = mode
        quality = self.test_parameter(parameter_test)
        if quality >= now_quality:
            now_quality = quality
            parameter_ls.append(parameter_test.copy())
            parameter_Q.append(quality)
        else:
            parameter_test[8] = last_parametar
    print("mode test is over")

    # ###################### G test #######################
    test_point = parameter_test[1]
    combins = self.get_isolated(test_point, self.select_No)
    total_len = len(combins)
    progress = 0

    for com in combins:
        if quality == 4:
            return self.data_process.parameter_save(parameter_ls, parameter_Q)

        if parameter_test[1] in com:
            continue

        progress += 1
        message = "processing G points test {}...".format(com)
        ICT_general_function.processbar(progress, total_len, message)

        last_parametar = parameter_test[2:7]
        parameter_test[2:7] = com
        quality = self.test_parameter(parameter_test)
        if quality >= now_quality:
            now_quality = quality
            parameter_ls.append(parameter_test.copy())
            parameter_Q.append(quality)
        else:
            parameter_test[2:7] = last_parametar
    print("G test is over")

    # ###################### Rpt test #######################
    total_len = len(RPT)
    progress = 0
    "[hi, lo, G1, G2, G3, G4, G5, DLY, MODE, AVG, Rpt, OFFSET]"
    for Rpt in RPT:
        if quality == 4:
            return self.data_process.parameter_save(parameter_ls, parameter_Q)
        progress += 1
        message = "processing Rpt test, Rpt =  {}...".format(Rpt)
        ICT_general_function.processbar(progress, total_len, message)

        last_parametar = parameter_test[10]
        parameter_test[10] = Rpt
        quality = self.test_parameter(parameter_test)
        if quality >= now_quality:
            now_quality = quality
            parameter_ls.append(parameter_test.copy())
            parameter_Q.append(quality)
        else:
            parameter_test[10] = last_parametar
    print("Rpt test is over")

    # A-F組合調參
    print("parameter_ls = ", parameter_ls)
    print("parameter_Q = ", parameter_Q)

    self.data_process.parameter_save(parameter_ls, parameter_Q)


def tolerance_adj(up_limit, low_limit, plusLm, minusLm):
    # up_limit、low_limit:標準規格
    # plusLm、minusLm:現有規格
    if float(up_limit) > float(plusLm):
        input_high = up_limit
    else:
        input_high = plusLm
    if float(low_limit) < float(minusLm):
        input_low = low_limit
    else:
        input_low = minusLm

    app = Application().connect(path=r"C:\etr8001\etr8001.exe")  # 創建RPA物件
    dlg_spec = app.window(title_re=r".*Test Data Edit >.*")  # 創建RPA物件
    ICT_rpa = ICT_RPA.ICTPywin(dlg_spec)  # 二次封裝RPA物件，新增etr8001操作標準步驟方法
    ICT_rpa.tolerance_input(input_high, input_low)


def tolerance_read():
    app = Application().connect(path=r"C:\etr8001\etr8001.exe")  # 創建RPA物件
    dlg_spec = app.window(title_re=r".*Test Data Edit >.*")  # 創建RPA物件
    ICT_rpa = ICT_RPA.ICTPywin(dlg_spec)  # 二次封裝RPA物件，新增etr8001操作標準步驟方法
    plusLm, minusLm = ICT_rpa.read_tolerance()
    return plusLm, minusLm
