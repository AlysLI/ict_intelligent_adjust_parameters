# -*- coding: utf-8 -*-
"""
Common function
"""

def processbar(now_step, total_setp, message):
    process_ratio = now_step/total_setp
    a = "*" * round(20 * process_ratio)
    b = '.' * round(20 - 20 * process_ratio)
    c = process_ratio * 100
    print("\r{:^4.1f}%[{}-->{}]  {}/{} {}".format(c,a,b,now_step,total_setp,message), end="")
