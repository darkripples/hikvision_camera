#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2018/10/31
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   fls易用性utils

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2018/10/31 11:41   fls        1.0         create
"""

from .fls_log import fls_log
from .attrdict import AttrDict as fdic
from .fmt_utils import fmt_null_obj as fnull, e_string as fstr, e_int, e_int_money
from .date_utils import (fmt_date as fmt_date, get_day_n as after_date, get_seconds_n as after_seconds,
                         get_interval_day as interval_day, reformat_date_str as reformat_date_str)
from .date_utils import FMT_DATETIME, FMT_DATE, FMT_TIME, FMT_DATETIME_SEPARATE

from .read_conf_utils import read_conf

