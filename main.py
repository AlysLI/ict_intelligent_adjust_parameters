# -*- coding: utf-8 -*-
"""
RPA
"""
import threading

from ict.gui import ICT_GUI

if __name__ == '__main__':
    t1 = threading.Thread(target=ICT_GUI.GUI_start(), args=())
    t1.start()
