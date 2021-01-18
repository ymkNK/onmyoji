#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: function_factory.py
@time: 2021/1/18 14:47
@desc: 功能和数据模块
"""
from dataclasses import dataclass
import json

from configure_tools import Configure


@dataclass
class Procedure:
    proce_name: str
    proce_loc: tuple
    proce_color: tuple

    def __post_init__(self):
        ...

    def reset_loc_color(self, loc, color):
        """设置loc和color"""
        self.proce_loc = loc
        self.proce_color = color

    def get_proce_name(self):
        """获取流程名"""
        return self.proce_name

    def get_values(self):
        """获取 流程名 [(坐标), (颜色)]"""
        return self.proce_name, [self.proce_loc, self.proce_color]


@dataclass
class Function:
    func_name: str
    procedures: [Procedure]

    def __post_init__(self):
        # 初始化一个 p_name: p的字典
        self.proce_dict = {}
        for p in self.procedures:
            self.proce_dict[p.get_proce_name()] = p

    def get_procedure_names(self):
        return [p.get_proce_name() for p in self.procedures]

    def get_func_name(self):
        return self.func_name

    def get_data(self):
        """获取data"""
        result = {}
        for p in self.procedures:
            k, v = p.get_values()
            result[k] = v
        return result

    def get_json(self):
        """获取字典"""
        result = self.get_data()

        json_data = {
            'func_name': self.func_name,
            'data': result
        }

        return json_data

    def update(self, p_name, p_xy, p_color):
        """更新值"""
        p = self.proce_dict.get(p_name)
        assert isinstance(p, Procedure)
        p.reset_loc_color(p_xy, p_color)

    def save_function_to_json(self, path):
        """保存配置文件function到json"""
        data = self.get_json()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)


@dataclass
class FuncFactory:
    def __post_init__(self):
        self.cf = Configure('configures/functions.ini')

    def create_function_from_data(self, func_name, data):
        """普通创建function"""
        procedures = []
        for k, v in data.items():
            p = Procedure(k, v[0], v[1])
            procedures.append(p)
        return Function(func_name, procedures)

    def create_function_from_json(self, path):
        """从json文件创建Function实例"""
        with open(path, "r", encoding="UTF-8") as f_load:
            json_var = json.load(f_load)
        func_name = json_var['func_name']
        data = json_var['data']

        return self.create_function_from_data(func_name, data)

    def init_config(self, func_name, flag_index=1):
        """从config中读取数据，获取配置数据，初始化data"""
        # 获取功能名的编号
        flag = func_name[flag_index]
        names = self.cf.get_option(flag, 'indexs').split('-')
        data = {}
        for name in names:
            data[name] = ['', '']

        return self.create_function_from_data(func_name, data)
