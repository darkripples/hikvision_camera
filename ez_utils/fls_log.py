#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2016/6/7
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   fls易用性utils-log记录相关

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2016/06/07 11:41   fls        1.0         create
2019/10/24         fls        2.0         重构
2019/11/20         fls        2.1         优化 无handler_name的情况
"""

import logging
import os

from .date_utils import fmt_date, FMT_DATE


def _get_msg4log(*args):
    # Get LOG msg
    msg = ''
    try:
        if len(args) > 1:
            if "%" in args[0]:
                msg = args[0] % args[1:]
            else:
                msg = ' '.join([str(i) for i in args])
        elif len(args) == 1:
            msg = str(args[0])
        else:
            msg = ''
    except:
        msg = str(args)
    return msg


class FlsLog:
    # Write LOG
    def __init__(self, log_filepath=None, file_name=None, date_name=fmt_date(fmt=FMT_DATE)[:8],
                 handler_name='root', log_level=logging.DEBUG, show_console=True, write_file=True):
        if not log_filepath:
            log_filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        if not os.path.exists(log_filepath):
            os.makedirs(log_filepath)
        if not file_name:
            file_name = "darkripples"

        self.log_filepath = os.path.join(log_filepath, file_name + '.log.' + date_name)

        self.logger = logging.getLogger(handler_name or "MAIN")
        self.handlers = self.logger.handlers

        self.logger.setLevel(log_level)

        # 设置输出日志格式
        fmt_tmp = "%(asctime)s %(levelname)s %(name)s %(message)s"
        if not handler_name:
            # 无handler_name的话，也去掉%(name)s，否则会写为root
            fmt_tmp = "%(asctime)s %(levelname)s %(message)s"
        formatter = logging.Formatter(
            fmt=fmt_tmp,
            # 时间格式采用默认的，显性记录下datefmt
            datefmt=None
        )

        if not self.handlers:
            if write_file:
                fh = logging.FileHandler(self.log_filepath, encoding="utf-8")
                # 为handler指定输出格式
                fh.setFormatter(formatter)
                # 为logger添加的日志处理器
                self.logger.addHandler(fh)
            if show_console:
                # 显示控制台输出
                ch = logging.StreamHandler()
                # 为handler指定输出格式
                ch.setFormatter(formatter)
                # 为logger添加的日志处理器
                self.logger.addHandler(ch)

            self.handlers = self.logger.handlers

    def log_info(self, *args):
        # Write info msg
        self.logger.info(_get_msg4log(*args))

    def log_debug(self, *args):
        # Write debug msg
        self.logger.debug(_get_msg4log(*args))

    def log_warning(self, *args):
        # Write warning msg
        self.logger.warning(_get_msg4log(*args))

    def log_error(self, *args):
        # Write error msg
        self.logger.error(_get_msg4log(*args))


def fls_log(log_filepath=None, file_name='darkripples', handler_name='root', show_console=True, write_file=True):
    """
    实例化
    :param log_filepath:
    :param file_name:
    :param handler_name:
    :param show_console:
    :param write_file:
    :return:
    """
    return FlsLog(log_filepath=log_filepath, file_name=file_name, handler_name=handler_name, show_console=show_console,
                  write_file=write_file)


if __name__ == '__main__':
    # For test:
    a = fls_log()
    a.log_info('11212')
    a.log_debug('x')
    a.log_warning('11212')
    a.log_error('error:%s', 'test')
