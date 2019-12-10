#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2016/06/06
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   fls易用性utils-对象格式化相关utils

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2016/06/06 11:41   fls        1.0         create
"""


def __check_null(v):
    # Check 'v' for None
    if v and v not in ('None', 'null', 'Null'):
        return True
    return False


def __fmt_null_ListTuple(l_t):
    # Change 'None' to '' for List or Tuple
    return [fmt_null_obj(i) if __check_null(i) else '' for i in l_t]


def __fmt_null_Dict(d):
    # Change 'None' to '' for Dict
    return dict((k, fmt_null_obj(v)) if __check_null(v) else (k, '') for k, v in d.items())


def fmt_null_obj(obj):
    """将空对象转为空字符串(obj)
    \t\t@param: obj 传入对象
    """
    if not __check_null(obj): return ''
    if type(obj) in (list, tuple):
        # Change 'None' to ''
        obj_new = __fmt_null_ListTuple(obj)
    elif type(obj) == dict:
        # Change None's value to ''
        obj_new = __fmt_null_Dict(obj)
    else:
        obj_new = obj
    return obj_new


def e_string(value, buflen=0, align='L', fillchar=' '):
    """打包字符串，字符型字段填充(value , buflen = 0 , align='L' , fillchar = ' ')
    \t\t@param: value       字段内容
    \t\t@param: buflen      填充后总长度 
    \t\t@param: align       字段对齐(默认左对齐) L:左对齐 R:右对齐 C:居中
    \t\t@param: fillchar    填充字符(默认空格符)
    """
    if value is None:
        value = ''
    elif type(value) != str:
        value = str(value)
    if len(fillchar) != 1:
        raise RuntimeError('填充字符参数[fillchar]格式错误')
    if buflen > 0:
        if len(value) > buflen:
            raise RuntimeError('打包字段[%s]长度越界，要求长度为：%d，实际长度为：%d' % (value, buflen, len(value)))
        if align == 'L':
            return value.ljust(buflen, fillchar)
        elif align == 'R':
            return value.rjust(buflen, fillchar)
        elif align == 'C':
            return value.center(buflen, fillchar)
        else:
            raise RuntimeError('填充方向参数[align]格式错误，合法的参数为L、R、C')
    else:
        return value


def e_int(value, buflen=0, align='R', fillchar='0'):
    """ 打包整型，整型数值字段打包格式字符串
        参数列表：value:       字段内容
                  buflen:      填充后总长度 
                  align: 字段对齐(默认右对齐) L:左对齐 R:右对齐 C:居中
                  fillchar:    填充字符(默认空格符)
    """
    if value is None:
        value = 0
    tmpstr = str(int(value))
    return e_string(tmpstr, buflen, align, fillchar)


def e_int_money(value, buflen=0, align='R', fillchar='0'):
    """
     打包金额浮点，以分为单位的金额格式话
     \t\t@param: value       字段内容，整形或浮点型，以元为单位
     \t\t@param: buflen      填充后长度
     \t\t@param: align       对齐方式(默认右对齐) L:左对齐 R:右对齐 C:居中
     \t\t@param: fillchar    填充字符(默认空格符)
    """
    if value is None:
        value = 0
    if float(value) < 0:
        s = '-' + e_int(round(abs(value) * 100), buflen - 1, align, fillchar)
        return s
    else:
        return e_int(round(value * 100), buflen, align, fillchar)


def __test_2_fmt_null_obj():
    # Test for fmt_null_obj
    n = None
    a = [None, 'asdf', 123, '12']
    b = {'a': None, 'b': 'None', 'c': 1, 'd': '123'}
    c = [{'a': 'None', 'b': None, 'c': 123}, {'d': None, 'e': '123'}, b]
    d = [{'a': 'None', 'b': None, 'c': 123}, {'d': None, 'e': '123'}, c]
    old = d
    print(old)
    new_ = fmt_null_obj(old)
    print(new_)


def __test_2_fmt_date():
    # Test for fmt_date()
    a = fmt_date(fmt='%Y-%m-%d')
    import sys
    print(sys.argv)
    fmt = sys.argv[-1] if len(sys.argv) == 2 else '%Y-%m-%d'
    a = fmt_date(fmt=fmt)
    print(a)


def formatter(src: str, firstUpper: bool = False):
    """
    将下划线分隔的名字,转换为驼峰模式
    :param src:
    :param firstUpper: 转换后的首字母是否指定大写(如
    :return:
    """
    arr = src.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper() + i[1:]

    if not firstUpper:
        res = res[0].lower() + res[1:]
    return res


def allot_list(src_list: list, n: int) -> list:
    """
    根据给定的组数，分配list给每一组-顺序分组
    :param src_list: 源list
    :param n: 每n个分一组
    :return:
    """
    return [src_list[i:i + n] for i in range(0, len(src_list), n)]


def help(num='①'):
    print(num + "关于格式化")
    print("\tfNull(obj)")
    print("\t" + fmt_null_obj.__doc__)
    print("\tdmpStr(value, buflen = 0, align = 'L', fillchar = ' ')")
    print("\t" + e_string.__doc__)


if __name__ == '__main__':
    # For test:
    # __test_2_fmt_null_obj()
    __test_2_fmt_date()
