# !/usr/bin/env python
# coding:utf8
"""
@Time       :   2019/10/25
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   fls易用性utils-配置文件读取utils

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/10/25 15:12     fls        1.0         create
"""

import configparser
from .attrdict import AttrDict as fdic


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        """
        重写，原configparser模块会统一转参数为小写
        :param optionstr:
        :return:
        """
        return optionstr


def read_conf(file_path: str):
    """
    读取配置文件
    :param file_path:
    :return:
    """
    # cf = configparser.ConfigParser()
    cf = MyConfigParser()
    cf.read(file_path, encoding="utf8")

    ret = fdic()
    sections = cf.sections()
    for s in sections:
        sub_conf = cf.options(s)
        main_data = fdic()
        for v in sub_conf:
            main_data[v] = cf.get(s, v)
        # 将所有参数按层级放在fdic中
        ret[s] = main_data

    return ret
