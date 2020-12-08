# -*- coding: utf-8 -*-

import os

os.system(
"\
pyinstaller \
main.py \
--name ICT_smart_turning \
-i pics\\ICT.ico \
-p ict\\testlogic\\ICT_Testing_Mode.py \
-p ict\\testlogic\\R_mode_learning.py \
-p ict\\testlogic\\C_mode_learning.py \
-p ict\\testlogic\\D_mode_learning.py \
-p ict\\testlogic\\J_mode_learning.py \
-p ict\db_func\\ICT_syn_data.py \
-p ict\\rpa\\ICT_RPA.py \
-p ict\\gui\\ICT_GUI.py \
-p ict\dataprocessing\\ICT_GetData.py \
-p common\\ICT_general_function.py\
")
