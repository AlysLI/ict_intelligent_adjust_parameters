# -*- coding: utf-8 -*-
"""
Do preprocessing
"""
import numpy as np
import pandas as pd
import os
import time
import re
from itertools import combinations

from common import ICT_general_function
from common.ICT_base_data import ICT_base_data


class DataProcess():
    def __init__(self, location, program):
        self.step_total_info = []
        self.MeasV = 0
        self.Dev = 0
        self.__location = location
        self.__program = program
        self.__IAIpath = 'C:\\IAI_AI'
        self.__IAI_program_path = self.__IAIpath + '\\' + self.__program
        # 調參目標的程式資料夾路徑
        self.__path = self.__location+'\\'+self.__program
        self.parameter_col = ["Board_Name",
                              "Step",
                              "Type",
                              "ExpectV",
                              "+Lm%",
                              "-Lm%",
                              "HiP",
                              "LoP",
                              "G1",
                              "G2",
                              "G3",
                              "G4",
                              "G5",
                              "DLY",
                              "MODE",
                              "Avg",
                              "Rpt",
                              "OFFSET",
                              "MeasV",
                              "Dev",
                              "Quality"]
        self.__check_data()

    def find_step(self, step_info):
        if len(step_info) != 3:
            print("There is no step info...")
        else:
            step_data = pd.read_excel(self.__IAI_program_path
                                      + '\\Step_data.xlsx')
            Step_data = step_data[(step_data["Parts-N"].str.contains(step_info[0])) &
                                  (step_data["Hi-P"] == int(step_info[1])) &
                                  (step_data["Lo-P"] == int(step_info[2]))]
            if len(Step_data["Step"]) == 0:
                Step_data = step_data[(step_data["Parts-N"].str.contains(step_info[0])) &
                                      (step_data["Hi-P"] == int(step_info[2])) &
                                      (step_data["Lo-P"] == int(step_info[1]))]
            train_data = np.array(Step_data)
            self.step_total_info = train_data.tolist()
            self.step_total_info = self.step_total_info[0]
            self.__renwe_ICT_base_data(self.step_total_info)
            return self.step_total_info

    def find_step_OK(self, step):
        step_data = pd.read_excel(self.__IAI_program_path+'\\Step_data.xlsx')
        Step_data = step_data[step_data["Step"] == int(step)]

        measure = float(re.sub("[a-zA-Z]", "", self.MeasV))
        temp = []
        try:
            if isinstance(Step_data["ExpectV"].values[0], str):
                ExpectV = float(re.sub("[a-zA-Z]", "",
                                Step_data["ExpectV"].values[0]))
            else:
                ExpectV = Step_data["ExpectV"].values[0]

            if isinstance(Step_data["+Lm%"].values[0], str):
                plus_lim = float(re.sub("[a-zA-Z]", "",
                                 Step_data["+Lm%"].values[0]))
            else:
                plus_lim = Step_data["+Lm%"].values[0]

            if isinstance(Step_data["-Lm%"].values[0], str):
                minus_lim = float(re.sub("[a-zA-Z]", "",
                                  Step_data["-Lm%"].values[0]))
            else:
                minus_lim = Step_data["-Lm%"].values[0]
        except:
            temp.append(Step_data["ExpectV"].values[0])
            print(temp)
        upperbond = ExpectV * (1 + plus_lim/100)
        lowerbond = ExpectV * (1 - minus_lim/100)
        if lowerbond <= measure <= upperbond:
            return True
        else:
            return False

    def read_measure(self, step):
        step_count = 0
        with open(self.__IAI_program_path+"\\IAI_m.txt", 'rt') as f:
            for line in f:
                sp = line.split()
                if step+3 == step_count:
                    self.MeasV = sp[9]
                    if len(sp) == 11:
                        self.Dev = sp[10]
                    elif len(sp) == 12:
                        self.Dev = sp[11]
                    measure = float(re.sub("[a-zA-Z]", "", self.MeasV))
                    dev = float(re.sub("[a-zA-Z]", "", self.Dev))
                    break
                step_count += 1
        return measure, dev

    def get_isolated_combin(self, Highpoint, select_No):
        point_list = pd.read_excel(self.__IAI_program_path + '\\pin_parameter'
                                   + '\\'+str(Highpoint)+'.xlsx')
        point_list = point_list["Isolated_Point"].drop_duplicates(keep='first',
                                                                  inplace=False
                                                                  )
        combins = list(combinations(point_list, select_No))
        return combins

    def Cpk_cal(self, MeasV_list):
        sigma = 3
        ExpectV = float(re.sub("[a-zA-Z]", "", self.step_total_info[7]))
        # 若下限为0, 则使用上限反转负值替代
        usl = float(ExpectV)*(1 + float(self.step_total_info[8])/100)
        lsl = float(ExpectV)*(1 - float(self.step_total_info[9])/100)

        # 数据平均值
        u = np.mean(MeasV_list)
        # 数据标准差
        stdev = np.std(MeasV_list, ddof=1)

        cpu = (usl - u) / (sigma * stdev)
        cpl = (u - lsl) / (sigma * stdev)
        # 得出cpk
        cpk = min(cpu, cpl)
        return cpk

    def parameter_save(self, parameter_ls, parameter_Q):
        if os.path.isfile(self.__IAI_program_path +
                          "\\parameter_save\\{}.txt"
                          .format(self.step_total_info[2])):
            pass
        else:
            Parameter_save_data = pd.DataFrame(columns=self.parameter_col)
            Parameter_save_data.to_csv(self.__IAI_program_path +
                                       "\\parameter_save\\{}.txt"
                                       .format(self.step_total_info[2]),
                                       sep=' ',
                                       index=False)  # 存成txt
        #  讀取AI_para.txt文件，没有则创建，‘a’表示再次写入时不覆盖之前的内容
        f = open(self.__IAI_program_path + "\\parameter_save\\{}.txt"
                 .format(self.step_total_info[2]), 'a')
        for i in range(len(parameter_ls)):
            result = []
            result.append(self.step_total_info[1])  # Board_name
            result.append(self.step_total_info[2])  # step
            result.append(self.step_total_info[6])  # type
            result.append(ICT_base_data.ExpectV)  # ExpectV
            result.append(self.step_total_info[8])  # +Lm%
            result.append(self.step_total_info[9])  # -Lm%
            # HiP LoP G1 G2 G3 G4 G5 DLY MODE Avg Rpt OFFSET
            for j in range(len(parameter_ls[0])):
                result.append(parameter_ls[i][j])
            result.append(self.MeasV)               # MeasV
            result.append(self.Dev)                 # Dev%
            result.append(parameter_Q[i])           # Quality

            for word in result:
                f.write(str(word))
                f.write(' ')
            f.write('\n')  # 实现换行的功能
        f.close()

    def search_database(self, stepNO, target_quality):
        result_list = []
        with open(self.__IAI_program_path+"\\parameter_save\\{}.txt"
                  .format(stepNO), 'rt') as f:
            for line in f:
                sp = line.split()
                if sp[20] == str(target_quality):
                    result_list.append(sp)
            return result_list

    def __mkdir(self, path):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # make dirs 创建文件时如果路径不存在会创建这个路径
            print("---  new {}...  ---".format(str(path)))
        else:
            print("---  There is this folder!  ---")

    def __check_data(self):
        # 判斷RPA基本資料是否存在
        self.__mkdir(self.__IAIpath)
        self.__mkdir(self.__IAI_program_path)
        self.__mkdir(self.__IAI_program_path + '\\' + 'pin_parameter')
        self.__mkdir(self.__IAI_program_path + '\\' + 'parameter_save')

        # 處理 raw data
        if os.path.isfile(self.__IAI_program_path+'\\Step_data.xlsx'):
            print("step_data.xlsx 檔案已存在。")
        else:
            self.__get_step_data(self.__program+'.dat')

        if os.path.isfile(self.__IAI_program_path+'\\group_data.xlsx'):
            print("Group data 檔案已存在")
        else:
            self.__get_group_data(self.__program+'.spa')

        if os.path.isfile(self.__IAI_program_path+'\\Device_data.xlsx'):
            print("Device_data.xlsx 檔案已存在。")
        else:
            self.__get_device_data('Pins.asc',
                                   self.__program+'.fsd',
                                   self.__program+'.icn')

        # 生成測試參數集
        if os.listdir(self.__IAI_program_path + '\\' + 'pin_parameter'):
            print("pin_parameter 檔案已存在。")
        else:
            self.__get_isolated_point()

        if os.listdir(self.__IAI_program_path + '\\' + 'parameter_save'):
            print("parameter save 檔案已存在。")

    def __get_step_data(self, file):
        start = time.time()
        # 基本元件測試參數
        Col_name_Base_el = ["Board_Name",
                            "Step",
                            "Parts-N",
                            "Hi-P",
                            "Lo-P",
                            "Type",
                            "ExpectV",
                            "+Lm%",
                            "-Lm%",
                            "DLY",
                            "MODE",
                            "OFFSET",
                            "G1",
                            "G2",
                            "G3",
                            "G4",
                            "G5",
                            "Skip",
                            "AVGE",
                            "RPT"]
        step_data = pd.DataFrame(columns=Col_name_Base_el)
        posi = 1
        progress = 0

        file_size = -1
        for file_size, line in enumerate(open(self.__path+"\\" +
                                              file, 'rU')):
            file_size += 1

        with open(self.__path+"\\"+file, 'rt') as f:
            for line in f:
                message = "processing Step data ..."
                progress += 1
                ICT_general_function.processbar(progress, file_size, message)

                sp = line.split()
                step = "step"+str(posi)

                if len(sp) > 2 and sp[1] == "File" and sp[0] == "!":
                    pass
                    # unused parameter
                    # File_name = sp[3]
                if len(sp) > 2 and sp[1] == "Board" and sp[0] == "!":
                    Board_name = sp[3]
                if len(sp) == 17:
                    step_data.loc[step, "Board_Name"] = Board_name
                    step_data.loc[step, "Step"] = sp[0]
                    step_data.loc[step, "Parts-N"] = sp[1]
                    step_data.loc[step, "Hi-P"] = sp[4]
                    step_data.loc[step, "Lo-P"] = sp[5]
                    step_data.loc[step, "G1"] = sp[6]
                    step_data.loc[step, "G2"] = sp[7]
                    step_data.loc[step, "G3"] = sp[8]
                    step_data.loc[step, "G4"] = sp[9]
                    step_data.loc[step, "G5"] = sp[10]
                    step_data.loc[step, "Skip"] = sp[11]
                    step_data.loc[step, "Type"] = sp[12]
                if len(sp) == 12:
                    step_data.loc[step, "ExpectV"] = sp[1]
                    step_data.loc[step, "+Lm%"] = sp[2]
                    step_data.loc[step, "-Lm%"] = sp[3]
                    step_data.loc[step, "DLY"] = sp[4]
                    step_data.loc[step, "MODE"] = sp[5]
                    step_data.loc[step, "AVGE"] = sp[6]
                    step_data.loc[step, "RPT"] = sp[7]
                    step_data.loc[step, "OFFSET"] = sp[9]
                    posi += 1
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
        # 存成excel
        step_data.to_excel(self.__IAI_program_path+'\\Step_data.xlsx')

    def __get_group_data(self, file):
        start = time.time()
        # 接腳短路群
        group_data = pd.DataFrame()
        group_cal_len = 0
        progress = 0
        group_start = False

        file_size = -1
        for file_size, line in enumerate(open(self.__path+"\\" +
                                              file, 'rU')):
            file_size += 1

        with open(self.__path+"\\"+file, 'rt') as f:
            for line in f:
                message = "processing Group data ..."
                progress += 1
                ICT_general_function.processbar(progress, file_size, message)

                sp = line.split()

                if group_start:
                    for number in sp:
                        if str.isdigit(number):
                            group_cal_len += 1
                    if len(sp) == group_cal_len:
                        group_member_list.extend(sp)
                        group_cal_len = 0
                    else:
                        group_data[group_name] = pd.Series(group_member_list)
                        group_start = False
                        group_cal_len = 0
                if len(sp) == 2:
                    if sp[0] == "Group" and str.isdigit(sp[1]):
                        group_name = sp[0]+sp[1]
                        group_member_list = []
                        group_start = True
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
        # 存成excel
        group_data.to_excel(self.__IAI_program_path+'\\Group_data.xlsx')

    def __get_device_data(self, pin_file, device_file, chip_file):
        # 基本元件接腳參數
        Col_name_Device = ["Board_Name",
                           "component",
                           "Pin_No",
                           "Pin_Name",
                           "Node_No",
                           "Node_Name",
                           "Type",
                           "ExpectV"]
        Device_data = pd.DataFrame(columns=Col_name_Device)

        start = time.time()
        posi = 1
        flag = 0
        progress = 0
        flag2 = 0
        file_size = -1
        for file_size, line in enumerate(open(self.__path+"\\" +
                                              pin_file, 'rU')):
            file_size += 1

        with open(self.__path+"\\"+pin_file, 'rt') as f:
            for line in f:
                message = "processing device pin data ..."
                progress += 1
                ICT_general_function.processbar(progress, file_size, message)

                sp = line.split()
                Pin = "Pin"+str(posi)
                if flag == 0:
                    Board_Name = sp[0]
                    flag += 1
                if len(sp) == 3:
                    component_name = sp[1]
                if len(sp) == 7 and flag2 != 0:
                    Device_data.loc[Pin, "Board_Name"] = Board_Name
                    Device_data.loc[Pin, "component"] = component_name
                    Device_data.loc[Pin, "Pin_No"] = sp[0]
                    Device_data.loc[Pin, "Pin_Name"] = sp[1]
                    Device_data.loc[Pin, "Node_No"] = sp[6]
                    Device_data.loc[Pin, "Node_Name"] = sp[5]
                    posi += 1
                if len(sp) == 7 and flag2 == 0:
                    flag2 = 1
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
        # find device type
        start = time.time()
        posi = 0
        progress = 0
        file_size = -1
        for file_size, line in enumerate(open(self.__path+"\\" +
                                              device_file, 'rU')):
            file_size += 1

        with open(self.__path+"\\"+device_file, 'rt') as f:
            for line in f:
                message = "processing Device type data ..."
                progress += 1
                ICT_general_function.processbar(progress, file_size, message)
                sp_1 = line.split(" ", 1)
                component_name = sp_1[0].split("=", 1)
                component_name = component_name[1]
                try:
                    Device_info = sp_1[1].split(",")
                    device_type = self.__get_type(Device_info)
                    device_value = self.__get_value(Device_info)
                except:
                    device_type = ''
                    device_value = ''

                Device_data.loc[Device_data["component"] == component_name,
                                "Type"] = device_type
                Device_data.loc[Device_data["component"] == component_name,
                                "ExpectV"] = device_value
                device_type = ''
                posi += 1
        end = time.time()
        print("執行時間：%f 秒" % (end - start))

        start = time.time()
        posi = 0
        progress = 0
        file_size = len(Device_data["component"])
        for com in Device_data["component"]:
            message = "processing Device type data ..."
            progress += 1
            ICT_general_function.processbar(progress, file_size, message)

            mask = Device_data["component"] == com
            Device_temp = Device_data.loc[mask, "Type"]
            Device_temp = Device_temp.iloc[0]
            if pd.isnull(Device_temp):
                device_type = self.__get_type(com)
                Device_data.loc[mask, "Type"] = device_type
                device_type = ''
        end = time.time()
        print("執行時間：%f 秒" % (end - start))

        # find IC
        start = time.time()
        posi = 0
        progress = 0
        file_size = -1
        for file_size, line in enumerate(open(self.__path+"\\" +
                                              chip_file, 'rU')):
            file_size += 1

        with open(self.__path+"\\"+chip_file, 'rt') as f:
            for line in f:
                message = "processing IC data ..."
                progress += 1
                ICT_general_function.processbar(progress, file_size, message)

                sp = line.split()
                component_part = sp[1]
                mask = Device_data["component"] == component_part
                Device_data.loc[mask, "Type"] = "IC"
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
        Device_data.to_excel(self.__IAI_program_path+'\\Device_data.xlsx')

    def __get_isolated_point(self):
        Col_name_point = ["Node_No", "Isolated_Point", "Type", "ExpectV"]
        Point_data = pd.DataFrame(columns=Col_name_point)
        Pin_data = pd.read_excel(self.__IAI_program_path+'\\Device_data.xlsx')
        Base_el_data = pd.read_excel(self.__IAI_program_path+'\\Step_data.xlsx')
        posi = 0
        Point_count = 0
        sereached_point = []
        sereached_component = []
        sereached_point_for_a_component = []

        start = time.time()

        all_point = pd.concat([Base_el_data["Hi-P"],
                               Base_el_data["Lo-P"]], axis=0)  # 把所有測試點排成一行

        for Highpoint in all_point:
            posi += 1
            message = "processing all test Point ..."
            ICT_general_function.processbar(posi, len(all_point), message)

            sereached_component = []
            if Highpoint not in sereached_point:  # 剔除已搜尋過的腳位
                mask1 = Pin_data["Node_No"] == Highpoint  # 找出與此點連結之所有元件(有重複)
                mask2 = Pin_data["Type"] != "IC"  # 剔除IC
                componet_select = Pin_data.loc[mask1 & mask2, "component"]

                for now_component in componet_select:  # 搜尋每個元件除了Highpoint外所有腳位
                    sereached_point_for_a_component = [Highpoint]
                    if (now_component not in sereached_component):  # 剔除重複元件
                        Isolated_select_info = Pin_data[Pin_data["component"] == now_component]
                        Isolated_select = Isolated_select_info["Node_No"]
                        Isolated_value = Isolated_select_info["ExpectV"].drop_duplicates(keep='first',
                                                                                         inplace=False)
                        Isolated_value = Isolated_select_info["ExpectV"].drop_duplicates(keep='first',
                                                                                         inplace=False)
                        Isolated_value = Isolated_select_info["ExpectV"].drop_duplicates(keep='first',
                                                                                          inplace=False)
                        if len(Isolated_value) != 0:
                            Isolated_value = Isolated_value.iloc[0]
                        for now_isolated in Isolated_select:
                            mask = Pin_data["component"] == now_component
                            if now_isolated not in sereached_point_for_a_component:  # 剔除已加入候選隔離點的腳位
                                Point_data.loc[Point_count, "Node_No"] = Highpoint
                                Point_data.loc[Point_count, "Isolated_Point"] = now_isolated
                                Point_data.loc[Point_count, "ExpectV"] = Isolated_value
                                type_to_save = Pin_data.loc[mask, "Type"].drop_duplicates(keep='first', inplace=False)
                                if len(type_to_save) != 0:
                                    Point_data.loc[Point_count, "Type"] = type_to_save.iloc[0]
                                sereached_point_for_a_component.append(now_isolated)
                                Point_count += 1
                        sereached_component.append(now_component)
                sereached_point.append(Highpoint)
                Point_data = Point_data.drop_duplicates(subset=['Isolated_Point'], keep='first', inplace=False)
                Point_data.to_excel(self.__IAI_program_path + '\\pin_parameter' + '\\'+str(Highpoint)+'.xlsx')
                Point_data = pd.DataFrame(columns=Col_name_point)
        end = time.time()
        print("執行時間：%f 秒" % (end - start))

    def __get_value(self, Device_info):
        ExpectV = {}
        R_pattern1 = re.compile(r"OHM")
        C_pattern1 = re.compile(r"UF")
        C_pattern2 = re.compile(r"NF")
        C_pattern3 = re.compile(r"MF")
        L_pattern1 = re.compile(r"UH")
        L_pattern2 = re.compile(r"NH")
        L_pattern3 = re.compile(r"MH")

        for info in Device_info:
            if (re.search(R_pattern1, info)) is not None \
               or (re.search(C_pattern1, info)) is not None \
               or (re.search(C_pattern2, info)) is not None \
               or (re.search(C_pattern3, info)) is not None \
               or (re.search(L_pattern1, info)) is not None \
               or (re.search(L_pattern2, info)) is not None \
               or (re.search(L_pattern3, info)) is not None:
                ExpectV = info
        if ExpectV is None:
            ExpectV = ''
        return ExpectV

    def __get_type(self, Device_info):
        if isinstance(Device_info, list):
            type_info = Device_info[0]
            type_info = str(type_info)
        elif isinstance(Device_info, str):
            type_info = Device_info
        R_pattern1 = re.compile(r"R\d+")
        R_pattern2 = re.compile(r"X_R\d+")
        R_pattern3 = re.compile(r"GMBU\d+")
        C_pattern1 = re.compile(r"C\d+")
        C_pattern2 = re.compile(r"X_C\d+")
        C_pattern3 = re.compile(r"X_XC\d+")
        C_pattern4 = re.compile(r"XXC\d+")
        L_pattern1 = re.compile(r"L\d+")
        L_pattern2 = re.compile(r"XXU\d+")
        L_pattern3 = re.compile(r"XU\d+")
        L_pattern4 = re.compile(r"U\d+")
        L_pattern5 = re.compile(r"X_U\d+")
        J_pattern1 = re.compile(r"J\d+")
        J_pattern2 = re.compile(r"XJ\d+")
        J_pattern3 = re.compile(r"X_J\d+")
        J_pattern4 = re.compile(r"X_XJ\d+")
        J_pattern5 = re.compile(r"XXJ\d+")
        Q_pattern1 = re.compile(r"Q\d+")

        if type_info in ['RES', 'RNW-ISO', 'RNW']\
           or (re.search(R_pattern1, type_info)) is not None \
           or (re.search(R_pattern2, type_info)) is not None \
           or (re.search(R_pattern3, type_info)) is not None:
            return 'R'
        elif [type_info in ['INDUCT', 'FERRITE']
              or (re.search(L_pattern1, type_info)) is not None
              or (re.search(L_pattern2, type_info)) is not None
              or (re.search(L_pattern3, type_info)) is not None
              or (re.search(L_pattern4, type_info)) is not None
              or (re.search(L_pattern5, type_info)) is not None]:
            return 'L'
        elif type_info in ['XTAL', 'XFMR']:
            return 'X'
        elif [type_info == 'CAP'
              or (re.search(C_pattern1, type_info)) is not None
              or (re.search(C_pattern2, type_info)) is not None
              or (re.search(C_pattern3, type_info)) is not None
              or (re.search(C_pattern4, type_info)) is not None]:
            return 'C'
        elif type_info == 'LED':
            return 'LED'
        elif type_info == 'DIO':
            return 'DIO'
        elif [type_info == 'XTR'
              or (re.search(Q_pattern1, type_info)) is not None]:
            return 'Q'
        elif [type_info == 'J'
              or (re.search(J_pattern1, type_info)) is not None
              or (re.search(J_pattern2, type_info)) is not None
              or (re.search(J_pattern3, type_info)) is not None
              or (re.search(J_pattern4, type_info)) is not None
              or (re.search(J_pattern5, type_info)) is not None]:
            return 'J'
        else:
            return 'doesn\'t have type'

    def __combin_group(self):
        Group_data = pd.read_excel(self.__IAI_program_path+'\\Group_data.xlsx')
        group_name = Group_data.columns.values
        group_name = group_name[1:]
        posi = 0
        for group in group_name:
            posi += 1
            message = "processing {} ...".format(group)
            ICT_general_function.processbar(posi, len(group_name), message)

            group_member = Group_data[group].tolist()
            group_member = self.delete_nan(group_member)
            Col_name_point = ["Node_No", "Isolated_Point", "Type"]
            group_union = pd.DataFrame(columns=Col_name_point)
            for member in group_member:
                try:
                    member_pin = pd.read_excel(self.__IAI_program_path +
                                               '\\pin_parameter'+'\\{}.xlsx'
                                               .format(int(member)))
                    member_pin = member_pin[['Node_No',
                                             'Isolated_Point',
                                             'Type']]
                    group_union = group_union.append(member_pin)
                except:
                    print("No such file, {}".format(int(member)))
            group_union = group_union.drop_duplicates(subset=['Isolated_Point'],
                                                      keep='first',
                                                      inplace=False)
            group_union.to_excel(self.__IAI_program_path + '\\pin_parameter' +
                                 '\\{}.xlsx'.format(group))

    def delete_nan(self, a_list):
        clean_list = []
        for member in a_list:
            if str(member) == 'nan'\
               or str(member) == 'Nan'\
               or str(member) == 'NaN'\
               or str(member) == 'NAN':
                pass
            else:
                clean_list.append(member)
        return clean_list
    def __renwe_ICT_base_data(self, step_total_info):
        ICT_base_data.step_index = step_total_info[0]
        ICT_base_data.Board_name = step_total_info[1]
        ICT_base_data.step_No = step_total_info[2]
        ICT_base_data.PartsN = step_total_info[3]
        ICT_base_data.HiP = step_total_info[4]
        ICT_base_data.LoP = step_total_info[5]
        ICT_base_data.Type = step_total_info[6]
        ICT_base_data.ExpectV = step_total_info[7]
        ICT_base_data.plusLm = step_total_info[8]
        ICT_base_data.minusLm = step_total_info[9]
        ICT_base_data.DLY = step_total_info[10]
        ICT_base_data.MODE = step_total_info[11]
        ICT_base_data.OFFSET = step_total_info[12]
        ICT_base_data.G1 = step_total_info[13]
        ICT_base_data.G2 = step_total_info[14]
        ICT_base_data.G3 = step_total_info[15]
        ICT_base_data.G4 = step_total_info[16]
        ICT_base_data.G5 = step_total_info[17]
        ICT_base_data.skip = step_total_info[18]
        ICT_base_data.avge = step_total_info[19]
        ICT_base_data.RPT = step_total_info[20]

