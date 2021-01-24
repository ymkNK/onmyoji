#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: mk_factory.py
@time: 2020/8/31 17:25
@desc: 鼠标键盘模拟工场
"""
from mouse_action import MouseAction
from keyboard_action import KeyboardAction
from tip_time import TipTime
from configure_tools import Configure


class MKFactory:
    def __init__(self):
        self.m = MouseAction()
        self.k = KeyboardAction()
        self.t = TipTime()
        self.cf = Configure('configures/config.ini')
        self.state = True
        self.escape_steps = [1, 2, 3]

    def colorCheck(self, color, coordinate):
        """
        检查颜色是否对应，整个操作流程是否进行的标志
        :param color: r,g,b
        :param coordinate: 坐标：(x, y)
        """
        # 进行循环的时候检测是否满足循环条件，即按键颜色是否符合目标颜色
        if isinstance(color, str):
            rgb_list = [int(a) for a in color.split(',')]
        elif isinstance(color, tuple) or isinstance(color, list):
            rgb_list = color
        else:
            self.state = '颜色格式不对...', 'red'

        try:
            self.state = self.m.check_mouse_color(rgb_list, coordinate)
        except Exception as e:
            # print('配置文件中的数据有误，有一种可能是你导入的别人的配置，'
            #       '但是别人的配置的电脑分辨率跟你的不一致，才导致的。')
            self.state = '颜色匹配错误，坐标可能越界...', 'red'

        return self.state

    def l1(self, xy, is_random=True):
        """单击，停顿，是否随机"""
        self.t.tip()
        if is_random:
            x_bias, y_bias = self.t.get_mouse_bias()
            self.m.mouse_click(xy[0]+x_bias, xy[1]+y_bias)
        else:
            self.m.mouse_click(xy[0], xy[1])

    def ln(self, xy, times=None):
        """单击很多次"""
        if times is None:
            times = self.cf.get_option('mouse', 'mouse_multi_times', 'int')
        for i in range(self.t.get_times_randint(times)):
            self.l1(xy)

    def l2(self, xy):
        """双击，停顿"""
        self.t.tip()
        self.m.mouse_doubleclick(xy[0], xy[1])

    def r1(self, xy):
        """右键单击，停顿"""
        self.t.tip()
        self.m.mouse_right_click(xy[0], xy[1])

    def r2(self, xy):
        """右键双击，停顿"""
        self.t.tip()
        self.m.mouse_right_doubleclick(xy[0], xy[1])

    def k_str(self, strs):
        """输入str，停顿"""
        self.t.tip()
        self.k.key_input(strs)
