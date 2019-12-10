#!/usr/bin/env python
# coding:utf8
"""
@Time       :   2018/10/31
@Author     :   fls
@Contact    :   fls@darkripples.com
@Desc       :   fls易用性utils-属性型字典
                字典转为属性类

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2018/10/31 11:41   fls        1.0         create
"""

import textwrap
import io as cStringIO
import copy
from .fmt_utils import formatter


class AttrDict(object):
    """
    可使用属性访问内容的字典类
    """

    def __init__(self, initd=None, nocopy=True, kword=None, strict=False, hump=False):
        """
            initd       初始字典
            nocopy      是否复制初始字典（默认不复制以提高效率）
            kword       关键字，关键字保证数据的存在，并控制内容
            strict      是否严格处理，当为True时，不允许获取不存在的数据，否则返回None
            hump        是否转为驼峰命名的key
        """
        self._stack = []
        if initd and hump:
            initd_ = {}
            for k, v in initd.items():
                initd_[formatter(k)] = v
            initd = initd_
        if nocopy:
            self._dict = initd or {}
        else:
            self._dict = copy.deepcopy(initd or {})
        self.Keyword = kword
        self.strict = strict

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def __getattr__(self, key):
        try:
            return self.__dict__['_dict'][key]
        except KeyError:
            try:
                if self.Keyword and type(key) is str:
                    attr = getattr(self.Keyword, key)
                    return attr.default
                else:
                    raise AttributeError()
            except AttributeError:
                if self.__dict__['strict']:
                    raise KeyError(key)
                else:
                    return None

    def __setattr__(self, key, value):
        if key == '_dict':
            self.__dict__['_dict'] = value
            return
        if key == '_stack':
            self.__dict__['_stack'] = value
            return
        if key == 'Keyword':
            self.__dict__['Keyword'] = value
            return
        if key == 'strict':
            self.__dict__['strict'] = value
            return
        try:
            if self.Keyword and type(key) is str:
                attr = getattr(self.Keyword, key)
                self._dict[key] = attr.validate(key, value)
            else:
                self._dict[key] = value
        except AttributeError:
            self._dict[key] = value

    def __delattr__(self, key):
        if self._dict.get(key, None):
            del self._dict[key]

    def __copy__(self, memo):
        return self.to_dict()

    __deepcopy__ = __copy__

    def to_dict(self):
        d = copy.deepcopy(self._dict)
        return d

    def from_dict(self, d, nocopy=False):
        if type(d) is not dict:
            d = {}
        if nocopy:
            self._dict = d
        else:
            self._dict = copy.deepcopy(d)

    def get(self, key, *args):
        if type(key) is str:
            keys = key.split('.')
        else:
            keys = [key]
        dict1 = self._dict
        li = []
        for k1 in keys:
            if type(dict1) == AttrDict:
                dict1 = dict1._dict
            try:
                dict1 = getattr(dict1, k1)
            except:
                try:
                    dict1 = dict1[k1]
                except:
                    if args:
                        return args[0]
                    else:
                        return None
                        # raise KeyError('无法在对象[%s]中找到[%s]的值' % ( '.'.join(li), k1 ))
            li.append(k1)

        return dict1

    def push(self):
        self._stack.append(copy.deepcopy(self._dict))

    def pop(self):
        self._dict = self._stack.pop()

    def clear(self):
        self._dict.clear()

    def update(self, dic):
        self._dict.update(dic)

    def __str__(self):
        s = cStringIO.StringIO()
        s.write('AttrDict{\n')
        keys = self.keys()
        for key in sorted(keys):
            value = self._dict[key]
            r = repr(value)
            r = '\n'.join(textwrap.wrap(r))
            s.write('%s:%s\n' % (key, r))
        s.write('}\n')
        return s.getvalue()

    __repr__ = __str__

    def __getstate__(self):
        return self.to_dict()

    def __setstate__(self, arg):
        self.from_dict(arg)


def help(num):
    print(num + "AttrDict")
    print("\t__init__(initd=None, nocopy=True, kword=None, strict=False)")
    print("\t字典转为属性类")
    print("\t\t@param:\t initd 初始字典,默认为空")
    print("\t\t@param:\t nocopy 是否复制初始字典（默认不复制以提高效率）")
    print("\t\t@param:\t kword 关键字，关键字保证数据的存在，并控制内容")
    print("\t\t@param:\t strict 是否严格处理，当为True时，不允许获取不存在的数据，否则返回None")
