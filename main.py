#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2019/12/10
@Author     :   fls    
@Contact    :   fls@darkripples.com
@Desc       :   主入口

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/10 10:48   fls        1.0         create
"""

from os import path
from ez_utils import read_conf
from tools.HKCameraManage import HKCManage

BASE_DIR = path.dirname(path.abspath(__file__))


def get_screenshot(place_no, carNo):
    """
    截图一帧
    :param place_no: 业务参数-摄像头位置说明
    :param carNo: 业务参数-要监控的车号
    :return:
    """
    confObj = read_conf(path.join(BASE_DIR, "conf", "conf.ini"))
    confHK = confObj["HIKVISION_" + place_no]
    f = HKCManage(confHK.place, confHK.ip, eval(confHK.port), confHK.user, confHK.pwd)
    f.get_screenshot(carNo)


def videotape_seconds(place_no, carNo, t_seconds):
    """
    录制t_seconds秒
    :param place_no: 业务参数-摄像头位置说明
    :param carNo: 业务参数-要监控的车号
    :param t_seconds: 要录制的时间(秒)
    :return:
    """
    confObj = read_conf(path.join(BASE_DIR, "conf", "conf.ini"))
    confHK = confObj["HIKVISION_" + place_no]
    f = HKCManage(confHK.place, confHK.ip, eval(confHK.port), confHK.user, confHK.pwd)
    f.videotape_seconds(carNo, t_seconds)


def show(place_no):
    """
    预览
    :param place_no: 业务参数-摄像头位置说明
    :return:
    """
    confObj = read_conf(path.join(BASE_DIR, "conf", "conf.ini"))
    confHK = confObj["HIKVISION_" + place_no]
    f = HKCManage(confHK.place, confHK.ip, eval(confHK.port), confHK.user, confHK.pwd)
    f.show()


if __name__ == "__main__":
    # get_screenshot("01", "鲁A12345")
    # videotape_seconds("01", "鲁A12345", 10)
    show("01")
