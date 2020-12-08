# -*- coding: utf-8 -*-
from pywinauto.application import Application  # RPA
import time
import os
import pandas as pd
import re
from itertools import combinations

from ict.dataprocessing import ICT_GetData
from ict.rpa import ICT_RPA
from ict.testlogic import R_mode_learning
from ict.testlogic import C_mode_learning
from ict.testlogic import D_mode_learning
from ict.testlogic import J_mode_learning
from ict.testlogic import Testjet_mode_learning

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)


class ModeSelect():
    def __init__(self, location, program):
        self.__location = location
        self.__program = program
        self.__IAIpath = 'C:\\IAI_AI'
        self.__IAI_program_path = self.__IAIpath + '\\' + self.__program
        self.__tool_path = r"C:\etr8001\etr8001.exe"
        self.__window_name = r".*Test Data Edit >.*"
        self.data_process = ICT_GetData.DataProcess(self.__location,
                                                    self.__program)
        self.__app = Application().connect(path=self.__tool_path)  # 創建RPA物件
        self.__dlg_spec = self.__app.window(title_re=self.__window_name)
        # 二次封裝RPA物件，新增etr8001操作標準步驟方法
        self.__ICT_rpa = ICT_RPA.ICTPywin(self.__dlg_spec)
        self.__test_time = 1
        self.select_No = 1
        self.step_index = 0
        self.Board_name = 0
        self.step_No = 0
        self.PartsN = 0
        self.HiP = 0
        self.LoP = 0
        self.Type = 0
        self.ExpectV = 0
        self.plusLm = 0
        self.minusLm = 0
        self.DLY = 0
        self.MODE = 0
        self.OFFSET = 0
        self.G1 = 0
        self.G2 = 0
        self.G3 = 0
        self.G4 = 0
        self.G5 = 0
        self.skip = 0
        self.avge = 0
        self.RPT = 0
        self.MeasV = 0

        self.last_mode = 0  # 紀錄上次調到哪一個模式

    def fast_mode(self, select_No):
        self.select_No = select_No
        self.Continuous = True
        # # 第一次先讀有沒有IAI_measure檔案txt
        if os.path.isfile("C:\\IAI_AI"+"\\"+self.__program+"\\IAI_m.txt"):
            pass
        else:
            self.__ICT_rpa.save_MeasV(self.__program)
        self.__mode_process("快速模式")

    def learning_mode(self, select_No):
        self.select_No = select_No
        self.Continuous = True
        # # 第一次先讀有沒有IAI_measure檔案txt
        if os.path.isfile("C:\\IAI_AI"+"\\"+self.__program+"\\IAI_m.txt"):
            pass
        else:
            self.__ICT_rpa.save_MeasV(self.__program)
        self.__mode_process("學習模式")
        print("over")

    def __mode_process(self, test_mode):
        first_step = False  # 控制是否判斷當前步驟是否pass

        start_all = time.time()
        while(self.Continuous):  # start a step
            step_OK = False
            start = time.time()
            # 讀取此step info
            step_info = self.__ICT_rpa.find_step_info()
            # 10次讀不到就判已經最後一個fail
            if step_info == -100:  # 程式總調參結束訊號
                self.Continuous = False
                print("last step")
                end_all = time.time()
                print("總執行時間：%f 秒" % (end_all - start_all))
                break
            # 讀到步驟，開始讀取步驟訊息
            # 找step total info
            step_total_info = self.data_process.find_step(step_info)

            self.__renew_step_info(step_total_info)
            if first_step:
                self.__ICT_rpa.save_MeasV(self.__program)
                self.data_process.read_measure(self.step_No)  # 讀取測試值
                step_OK = self.data_process.find_step_OK(self.step_No)
                # 判斷步驟是否是fail的步驟，如果是OK的，則找下一個fail
                print('I am first step')
                if step_OK:
                    self.__ICT_rpa.next_fail()  # 到下一個step  ICT_RPA.next_fail()
                    # 讀取此step info
                    step_info = self.__ICT_rpa.find_step_info()
                    # 10次讀不到就判已經最後一個fail
                    if step_info == -100:  # 程式總調參結束訊號
                        self.Continuous = False
                        print("last step")
                        break
                    # 讀到步驟，開始讀取步驟訊息
                    step_total_info = self.data_process.find_step(step_info)  # 找step total info
                    self.__renew_step_info(step_total_info)
                    first_step = False
                    step_OK = False
                else:
                    first_step = False
                    step_OK = False
            print(step_total_info)

            if test_mode == "快速模式" and self.skip == 0:
                self.__database_select(test_mode)
                self.Continuous = False
            elif test_mode == "學習模式" and self.skip == 0:
                self.__select_and_test(test_mode)
            end = time.time()
            print("執行時間：%f 秒" % (end - start))
            time.sleep(0.5)

            just_fail = False
            if just_fail and self.Continuous:
                self.__ICT_rpa.next_fail()  # 到下一個fail step  ICT_RPA.next_fail()
            elif not just_fail and self.Continuous:
                self.__ICT_rpa.next_step()  # 到下一個step

    def __database_select(self, test_mode):
        # find step parameter from txt file
        target_quality_list = [0, 4]

        for target_quality in target_quality_list:
            parameter_list = self.data_process.search_database(self.step_No,
                                                               target_quality)
            # test parameter
            for parameter in parameter_list:
                parameter_to_test = []
                parameter_to_test.append(parameter[6])
                parameter_to_test.append(parameter[7])
                parameter_to_test.append(parameter[8])
                parameter_to_test.append(parameter[9])
                parameter_to_test.append(parameter[10])
                parameter_to_test.append(parameter[11])
                parameter_to_test.append(parameter[12])
                parameter_to_test.append(parameter[13])
                parameter_to_test.append(parameter[14])
                parameter_to_test.append(parameter[15])
                parameter_to_test.append(parameter[16])
                parameter_to_test.append(parameter[17])
                quality = self.test_parameter(parameter_to_test)
                # if return value == 2, 3, 4 ， parameter adjust success
                if quality >= 2:
                    print("I have done !")
                    return 0
        print("Fail !")

    def __select_and_test(self, test_mode):
        step_type = self.Type

        if step_type == 'J':
            J_mode_learning.jmodelearning(self)
        elif step_type == '0':
            Testjet_mode_learning.testjetmodelearning(self)
        elif step_type in ['Q', 'D', 'U', 'QF', 'HF']:
            D_mode_learning.dmodelearning(self)
        elif step_type == 'R':
            R_mode_learning.rmodelearning(self)
        elif step_type == 'C':
            C_mode_learning.cmodelearning(self)

        print("over")
        return 0

    def test_parameter(self, parameter_to_test):
        # test_parameter:需要照順序排列
        # output: step_OK:測試結果是否pass
        #         Cpk_pass: Cpk是否大於標準值
        #         Dev_OK: Dev是否有變小的趨勢
        Cpk_test_times = 5
        Cpk_standard = 10
        MeasV_list = []
        Dev_OK = False
        step_OK = False
        # 存測試值
        self.__ICT_rpa.save_MeasV(self.__program)
        # 讀取調參前測試值
        MeasV_old, Dev_old = self.data_process.read_measure(self.step_No)
        # 輸入參數+點擊測試
        self.__ICT_rpa.input_parameter(parameter_to_test, self.Type, self.last_mode)
        # 存測試值
        self.__ICT_rpa.save_MeasV(self.__program)
        # 讀取調參後測試值
        MeasV_new, Dev_new = self.data_process.read_measure(self.step_No)
        self.MeasV = MeasV_new
        # 判斷OK
        step_OK = self.data_process.find_step_OK(self.step_No)

        if abs(Dev_old) > abs(Dev_new):
            Dev_OK = True
        else:
            Dev_OK = False

        if step_OK:
            MeasV_list = []
            print("step pass, Cpk calculating...")
            for i in range(Cpk_test_times-1):
                self.__ICT_rpa.one_test()
                self.__ICT_rpa.save_MeasV(self.__program)
                MeasV_new, Dev_new = self.data_process.read_measure(self.step_No)
                self.MeasV = MeasV_new
                MeasV_list.append(MeasV_new)

            Cpk = self.data_process.Cpk_cal(MeasV_list)
            print("Cpk = ", Cpk)
            if Cpk >= Cpk_standard:
                self.last_mode = parameter_to_test[8]
                return 4
            else:
                self.last_mode = parameter_to_test[8]
                if Dev_OK:
                    return 3
                else:
                    return 2
        else:
            self.last_mode = parameter_to_test[8]
            if Dev_OK:
                return 1
            else:
                return 0

    def get_isolated(self, test_point, select_No):
        MAXIMUM_POINT_TO_SEARCH = 5
        combins = []
        final_combins = []
        five_point_list = []
        five_point_value = []
        five_point_type = []
        point_list = pd.read_excel(self.__IAI_program_path + '\\pin_parameter' +
                                   '\\'+str(test_point)+'.xlsx')

        R_point_list = point_list[point_list["Type"] == "R"].reset_index(drop=True)
        C_point_list = point_list[point_list["Type"] == "C"].reset_index(drop=True)
        L_point_list = point_list[point_list["Type"] == "L"].reset_index(drop=True)

        if self.Type == "R":
            for i in range(len(R_point_list)):
                unit = R_point_list.loc[i, "ExpectV"]
                value = self.__process_unit(unit)
                if value != value:
                    continue
                if len(five_point_list) < MAXIMUM_POINT_TO_SEARCH and value != "None":
                    five_point_list.append(R_point_list.loc[i, "Isolated_Point"])
                    five_point_value.append(value)
                    five_point_type.append("R")
                else:
                    for ii in range(MAXIMUM_POINT_TO_SEARCH):
                        if value > five_point_value[ii]:
                            five_point_list[ii] = R_point_list.loc[i, "Isolated_Point"]
                            five_point_value[ii] = value
                            five_point_type[ii] = "R"
                            break
            if len(five_point_list) < MAXIMUM_POINT_TO_SEARCH:
                for i in range(len(C_point_list)):
                    unit = C_point_list.loc[i, "ExpectV"]
                    value = self.__process_unit(unit)
                    if value != value:
                        continue
                    if len(five_point_list) < MAXIMUM_POINT_TO_SEARCH:
                        five_point_list.append(C_point_list.loc[i, "Isolated_Point"])
                        five_point_value.append(value)
                        five_point_type.append("C")
                    else:
                        for ii in range(MAXIMUM_POINT_TO_SEARCH):
                            if value > five_point_value[ii] and five_point_type[ii] == "C":
                                five_point_list[ii] = C_point_list.loc[i, "Isolated_Point"]
                                five_point_value[ii] = value
                                five_point_type[ii] = "C"
                                break
            if len(five_point_list) < MAXIMUM_POINT_TO_SEARCH:
                for i in range(len(L_point_list)):
                    unit = L_point_list.loc[i, "ExpectV"]
                    value = self.__process_unit(unit)
                    if value != value:
                        continue
                    if len(five_point_list) < MAXIMUM_POINT_TO_SEARCH:
                        five_point_list.append(L_point_list.loc[i, "Isolated_Point"])
                        five_point_value.append(value)
                        five_point_type.append("L")
                    else:
                        for ii in range(MAXIMUM_POINT_TO_SEARCH):
                            if value > five_point_value[ii] and five_point_type[ii] == "L":
                                five_point_list[ii] = L_point_list.loc[i, "Isolated_Point"]
                                five_point_value[ii] = value
                                five_point_type[ii] = "L"
                                break
        if select_No != 0:
            for i in range(select_No):
                combins.extend(list(combinations(five_point_list, i)))
            for com in combins:
                com_list = list(com)
                NO_of_G = len(com)
                for i in range(5-NO_of_G):  # G 補滿
                    com_list.append(0)
                final_combins.append(com_list)
        else:
            final_combins = [[0, 0, 0, 0, 0]]
        return final_combins

    def __process_unit(self, unit):
        R_pattern1 = re.compile(r"OHM")
        C_pattern1 = re.compile(r"UF")
        C_pattern2 = re.compile(r"NF")
        C_pattern3 = re.compile(r"MF")
        L_pattern1 = re.compile(r"UH")
        L_pattern2 = re.compile(r"NH")
        L_pattern3 = re.compile(r"MH")
        amptitude = 1

        if unit != unit:
            return float('nan')

        if (re.search(R_pattern1, unit)) is not None:
            unit_str = unit.split("OHM", 1)
            unit_str = unit_str[0].split(" ", 1)
            try:
                unit_str_temp = unit_str[1].strip()
                unit_str_temp2 = unit_str[0].strip()
                if unit_str_temp == "K":
                    amptitude = 1000
                if unit_str_temp2[-1] == "K":
                    unit_str[0] = unit_str[0].strip("K")
                    amptitude = 1000
            except:
                pass
            unit_temp = amptitude * float(unit_str[0])
        elif(re.search(C_pattern1, unit)) is not None:
            unit_str = unit.split("UF", 1)
            amptitude = 0.000001
            unit_temp = amptitude * float(unit_str[0])
        elif(re.search(C_pattern2, unit)) is not None:
            unit_str = unit.split("NF", 1)
            amptitude = 0.000000001
            unit_temp = amptitude * float(unit_str[0])
        elif(re.search(C_pattern3, unit)) is not None:
            unit_str = unit.split("MF", 1)
            amptitude = 0.001
            unit_temp = amptitude * float(unit_str[0])
        elif(re.search(L_pattern1, unit)) is not None:
            unit_str = unit.split("UH", 1)
            amptitude = 0.000001
            unit_temp = amptitude * float(unit_str[0])
        elif(re.search(L_pattern2, unit)) is not None:
            unit_str = unit.split("NH", 1)
            amptitude = 0.000000001
            unit_temp = amptitude * float(unit_str[0])
        elif(re.search(L_pattern3, unit)) is not None:
            unit_str = unit.split("MH", 1)
            amptitude = 0.001
            unit_temp = amptitude * float(unit_str[0])
        return unit_temp

    def __renew_step_info(self, step_total_info):
        self.step_index = step_total_info[0]
        self.Board_name = step_total_info[1]
        self.step_No = step_total_info[2]
        self.PartsN = step_total_info[3]
        self.HiP = step_total_info[4]
        self.LoP = step_total_info[5]
        self.Type = step_total_info[6]
        self.ExpectV = step_total_info[7]
        self.plusLm = step_total_info[8]
        self.minusLm = step_total_info[9]
        self.DLY = step_total_info[10]
        self.MODE = step_total_info[11]
        self.last_mode = self.MODE
        self.OFFSET = step_total_info[12]
        self.G1 = step_total_info[13]
        self.G2 = step_total_info[14]
        self.G3 = step_total_info[15]
        self.G4 = step_total_info[16]
        self.G5 = step_total_info[17]
        self.skip = step_total_info[18]
        self.avge = step_total_info[19]
        self.RPT = step_total_info[20]
