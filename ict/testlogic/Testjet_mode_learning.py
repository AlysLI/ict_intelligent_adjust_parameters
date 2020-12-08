# -*- coding: utf-8 -*-
from pywinauto.application import Application  # RPA
import re

from common import ICT_general_function
from common.ICT_base_data import ICT_base_data
from ict.rpa import ICT_RPA

def testjetmodelearning(self):
    # if Low-V > 10 fF  , Low-V == 10fF
    step_ExpextV = self.ExpectV
    number_part = re.findall(r"\d+\.?\d*", step_ExpextV)
    number_part = number_part[0]
    if len(number_part) == len(step_ExpextV):
        unit_part = ""
    else:
        unit_part = step_ExpextV[len(number_part):]
    number_part = float(number_part)

    # ###################### Low-V check #######################
    if not (unit_part == 'fF' and number_part < 10):
        app = Application().connect(path=r"C:\etr8001\etr8001.exe")  # 創建RPA物件
        dlg_spec = app.window(title_re=r".*Test Data Edit >.*")  # 創建RPA物件
        ICT_rpa = ICT_RPA.ICTPywin(dlg_spec)  # 二次封裝RPA物件，新增etr8001操作標準步驟方法
        ICT_rpa.Low_V_change()
        ICT_base_data.ExpectV = 10

    parameter_ls = [[self.HiP, self.LoP, self.G1, self.G2, self.G3, self.G4,
                     self.G5, self.DLY, self.MODE, self.avge, self.RPT,
                     self.OFFSET]]
    parameter_Q = [0]

    return self.data_process.parameter_save(parameter_ls, parameter_Q)
