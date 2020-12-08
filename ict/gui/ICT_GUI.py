# -*- coding: utf-8 -*-
"""
Operating GUI
"""
try:
    import Tkinter as tk
except:
    import tkinter as tk

import time
import threading
import sys

from ict.testlogic import ICT_Testing_Mode
from ict.db_func import ICT_syn_data


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        SampleApp.app = self
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self._frame.pack_propagate(0)


class StartPage(tk.Frame):
    def __init__(self, master):
        self.program_path = r'C:\etr8001'
        # self.program_test = r'R1684204-F0-V1'
        self.program_test = r'R1669407-B0-V2'

        master.title("ICT智能調參")
        tk.Frame.__init__(self, master, width=400, height=220)
        self.lb = tk.Label(self,
                           text="開始:開始測試  \n資料同步:同步資料庫資料",
                           font=('Helvetica', 20, "bold"))
        self.lb.pack(side=tk.TOP)
        self.btn = tk.Button(self,
                             text="開始",
                             font=('Helvetica', 15),
                             command=lambda: self.select_mode_to_run())
        self.btn.pack(side=tk.LEFT, expand=1, ipadx=10, padx=20)
        self.btn1 = tk.Button(self,
                              text="資料同步",
                              font=('Helvetica', 15),
                              command=lambda: thread_it(ICT_syn_data.SynData,
                                                        StartPage,
                                                        self.program_name_entry.get()))
        self.btn1.pack(side=tk.LEFT,
                       expand=1,
                       ipadx=10,
                       padx=20)
        self.btn2 = tk.Button(self,
                              text="結束程式",
                              font=('Helvetica', 15),
                              command=lambda: sys.exit())
        self.btn2.pack(side=tk.LEFT, expand=1, ipadx=10, padx=20)

        self.etr_position_frame = tk.Frame(master)
        self.etr_position_frame.pack(side=tk.TOP)
        self.etr_position_label = tk.Label(self.etr_position_frame,
                                           text='etr8001 程式位置')
        self.etr_position_label.pack(side=tk.LEFT)
        self.etr_position_entry = tk.Entry(self.etr_position_frame)
        self.etr_position_entry.insert(0, self.program_path)
        self.etr_position_entry.pack(side=tk.LEFT)

        self.program_name_frame = tk.Frame(master)
        self.program_name_frame.pack(side=tk.TOP)
        self.program_name_label = tk.Label(self.program_name_frame,
                                           text='測試程式名稱')
        self.program_name_label.pack(side=tk.LEFT)
        self.program_name_entry = tk.Entry(self.program_name_frame)
        self.program_name_entry.insert(0, self.program_test)
        # self.program_name_entry.insert(0, r'R1684204-F0-V1')
        self.program_name_entry.pack(side=tk.LEFT)

        self.mode_frame = tk.Frame(master)
        self.mode_frame.pack(side=tk.TOP)
        self.var = tk.StringVar()
        self.var.set('N')
        self.mode_print = tk.Label(self.mode_frame,
                                   bg='gray',
                                   width=50,
                                   text='請選擇調參模式')
        self.mode_print.pack()
        r1 = tk.Radiobutton(self.mode_frame,
                            text='快速模式',
                            variable=self.var,
                            value='快速模式',
                            command=lambda: self.print_select_mode_info())
        r1.pack(side=tk.LEFT, expand=1)
        r2 = tk.Radiobutton(self.mode_frame,
                            text='學習模式',
                            variable=self.var,
                            value='學習模式',
                            command=lambda: self.print_select_mode_info())
        r2.pack(side=tk.LEFT, expand=1)

        self.G_count = 0
        self.G_frame = tk.Frame(master)
        self.G_frame.pack(side=tk.TOP)
        self.v1 = tk.StringVar()
        self.v1.set('N')
        self.v2 = tk.StringVar()
        self.v2.set('N')
        self.v3 = tk.StringVar()
        self.v3.set('N')
        self.v4 = tk.StringVar()
        self.v4.set('N')
        self.v5 = tk.StringVar()
        self.v5.set('N')
        lis = ['G1', 'G2', 'G3', 'G4', 'G5']
        self.G_print = tk.Label(self.G_frame,
                                bg='gray',
                                width=50,
                                text='請選擇隔離點')
        self.G_print.pack()
        G1 = tk.Checkbutton(self.G_frame,
                            text=lis[0],
                            onvalue=lis[0],
                            variable=self.v1,
                            command=lambda: self.print_select_G_info())
        G1.pack(side=tk.LEFT, expand=1)
        G2 = tk.Checkbutton(self.G_frame,
                            text=lis[1],
                            onvalue=lis[1],
                            variable=self.v2,
                            command=lambda: self.print_select_G_info())
        G2.pack(side=tk.LEFT, expand=1)
        G3 = tk.Checkbutton(self.G_frame,
                            text=lis[2],
                            onvalue=lis[2],
                            variable=self.v3,
                            command=lambda: self.print_select_G_info())
        G3.pack(side=tk.LEFT, expand=1)
        G4 = tk.Checkbutton(self.G_frame,
                            text=lis[3],
                            onvalue=lis[3],
                            variable=self.v4,
                            command=lambda: self.print_select_G_info())
        G4.pack(side=tk.LEFT, expand=1)
        G5 = tk.Checkbutton(self.G_frame,
                            text=lis[4],
                            onvalue=lis[4],
                            variable=self.v5,
                            command=lambda: self.print_select_G_info())
        G5.pack(side=tk.LEFT, expand=1)

        self.control_panal = tk.Frame(master)
        self.control_panal.pack(side=tk.TOP)
        self.control_panal_print = tk.Label(self.control_panal,
                                            bg='gray',
                                            width=50,
                                            text='調參控制選項')
        self.control_panal_print.pack(side=tk.TOP)

        # 以下功能尚未完工
        self.fail_only = tk.StringVar()
        self.fail_only.set('N')
        self.one_step_only = tk.StringVar()
        self.one_step_only.set('N')
        just_fail = tk.Checkbutton(self.control_panal,
                                   text="Fail Only",
                                   onvalue=lis[0],
                                   variable=self.fail_only,
                                   command=lambda: self.print_control_info())
        just_fail.pack(side=tk.LEFT, expand=1)
        one_step = tk.Checkbutton(self.control_panal,
                                  text="One step Only",
                                  onvalue=lis[0],
                                  variable=self.one_step_only,
                                  command=lambda: self.print_control_info())
        one_step.pack(side=tk.LEFT, expand=1)
        # 以上功能尚未完工

        self.text_frame = tk.Frame(master)
        self.text_frame.pack(side=tk.TOP)
        self.show_anything = tk.Text(self.text_frame, height=5)
        self.show_anything.pack()

        self.Progressbar = tk.Frame(master)
        self.Progressbar.pack(side=tk.TOP)
        label1 = tk.Label(self.Progressbar,
                          text="同步進度:")
        label1.pack()
        self.canvas = tk.Canvas(self.Progressbar,
                                width=465,
                                height=22,
                                bg='white')
        self.canvas.place(x=110, y=60)
        self.canvas.pack()

        self.btn_download = tk.Button(self.Progressbar,
                                      text='啟動進度條',
                                      command=lambda: self.progress_my())
        self.btn_download.place(x=400, y=105)
        self.btn_download.pack()

        # 显示下载进度
    def progress_my(self):
        # 清空进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23,
                                                 width=0,
                                                 fill="white")
        x = 500  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        # for t in range(x):
        n = 465
        # 以矩形的长度作为变量值更新
        self.canvas.coords(fill_line, (0, 0, n, 60))
        self.Progressbar.update()
        time.sleep(0)  # 时间为0，即飞速清空进度条

        # 填充进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23,
                                                 width=0,
                                                 fill="green")
        x = 50  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        for i in range(x):
            n = n + 465 / x
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.Progressbar.update()
            time.sleep(0.02)  # 控制进度条流动的速度

    def call_count(self):
        print(self.v1.get())
        print(self.v2.get())
        print(self.v3.get())
        print(self.v4.get())
        print(self.v5.get())

    def print_select_mode_info(self):
        path = self.etr_position_entry.get()
        program = self.program_name_entry.get()
        mode = self.var.get()
        if mode == '快速模式' or mode == '學習模式':
            self.mode_print.config(text=path+'\\'+program+'...已選擇 '
                                   + self.var.get(),
                                   bg='gray')

    def print_control_info(self):
        pass

    def print_select_G_info(self):
        v1 = self.v1.get()
        v2 = self.v2.get()
        v3 = self.v3.get()
        v4 = self.v4.get()
        v5 = self.v5.get()
        self.G_count = 0
        if v1 == 'G1':
            self.G_count += 1
        if v2 == 'G2':
            self.G_count += 1
        if v3 == 'G3':
            self.G_count += 1
        if v4 == 'G4':
            self.G_count += 1
        if v5 == 'G5':
            self.G_count += 1
        self.G_print.config(text='已選擇 {} 個隔離點'.format(self.G_count), bg='gray')

    def select_mode_to_run(self):
        path = self.etr_position_entry.get()
        program = self.program_name_entry.get()
        mode = self.var.get()
        ICT_test_mode = ICT_Testing_Mode.ModeSelect(path, program)
        if mode == '快速模式':
            self.show_anything.insert('insert', '快速模式執行中...')
            thread_it(ICT_test_mode.fast_mode, self.G_count)
        elif mode == '學習模式':
            self.show_anything.insert('insert', '學習模式執行中...')
            thread_it(ICT_test_mode.learning_mode, self.G_count)
        else:
            self.mode_print.config(text='請選擇以下任一模式', bg='red')

    def do_something(self):
        print('IIIIIIIIIIIIIIIIIIIIIII')


def thread_it(func, *args):
    # 將函数打包進線程，防止GUI卡住
    # 創建
    t = threading.Thread(target=func, args=args)
    # 守護 !!!
    t.setDaemon(True)
    # 啟動
    t.start()
    # 阻塞--卡死界面！
    # t.join()


# ####  to be called  #####################
def GUI_start():   # to be called by main.py
    app = SampleApp()
    app.mainloop()
# ####  to be called  #####################
