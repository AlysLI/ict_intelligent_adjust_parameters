# -*- coding: utf-8 -*-
from common import ICT_general_function


def jmodelearning(self):
    parameter_test = []
    parameter_ls = [[self.HiP, self.LoP, self.G1, self.G2, self.G3, self.G4,
                     self.G5, self.DLY, self.MODE, self.avge, self.RPT,
                     self.OFFSET]]
    parameter_Q = [0]

    MODE = [0, 1, 2]
    now_quality = 0.1  # can be any number <1

    quality = self.test_parameter(parameter_ls[0])
    if quality >= now_quality:
        now_quality = quality
    if quality == 4:
        return self.data_process.parameter_save(parameter_ls, parameter_Q)

    parameter_test = [self.HiP, self.LoP, 0, 0, 0, 0, 0, 0, self.MODE, 0, 0, 0]
    # ###################### mode test #######################
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

    self.data_process.parameter_save(parameter_ls, parameter_Q)
