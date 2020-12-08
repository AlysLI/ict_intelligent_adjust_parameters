# -*- coding: utf-8 -*-
from common import ICT_general_function


def dmodelearning(self):
    parameter_test = []
    parameter_ls = [[self.HiP, self.LoP, self.G1, self.G2, self.G3, self.G4,
                     self.G5, self.DLY, self.MODE, self.avge, self.RPT,
                     self.OFFSET]]
    parameter_Q = [0]

    DLY = [0, 50, 100]
    RPT = [0, 1, 2, 3]
    now_quality = 0.1  # can be any number <1

    quality = self.test_parameter(parameter_ls[0])
    if quality >= now_quality:
        now_quality = quality
    if quality == 4:
        return self.data_process.parameter_save(parameter_ls, parameter_Q)

    parameter_test = [self.HiP, self.LoP, 0, 0, 0, 0, 0, 0, self.MODE, 0, 0, 0]
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

    self.data_process.parameter_save(parameter_ls, parameter_Q)
