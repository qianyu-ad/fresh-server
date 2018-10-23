"""
公共函数
"""

import os
import re
import time
import uuid
import hashlib
import base64
import random
import string
import datetime
import xlwt
from functools import wraps
from inspect import signature
from fresh.config.default import DOWN_DIR

# pylint: disable=all

def fmt_datetime(dt, fmt='%F %T'):
    return dt.strftime(fmt)


def get_current_time(fmt="%F %T"):
    """ 获取当前时间字符串"""
    now = datetime.datetime.now()
    return fmt_datetime(now, fmt)


def get_uuid(length=16):
    uid = str(uuid.uuid1()).encode('utf8')
    return hashlib.md5(uid).hexdigest()[:length]


def get_code(length=6, code_type='int'):
    """ 获取短信验证码
    :param length: 返回长度
    :param code_type: 返回类型
    """
    alpha = string.digits if code_type == 'int' else string.ascii_lowercase
    code = random.sample(alpha, length)
    code = ''.join(code)
    return code


def sha1_hash(text):
    """ sha1加密"""
    text = to_bytes(text)
    return hashlib.sha1(text).hexdigest()


def encode(text):
    """ base64 加密"""
    text = to_bytes(text)
    return base64.b64encode(text)


def decode(text):
    """ base64 解密"""
    text = to_bytes(text)
    return base64.b64decode(text)


def get_time():
    """ 获取时间戳"""
    return int(time.time())


def to_bytes(text):
    """ 转成bytes"""
    if isinstance(text, str):
        text = text.encode('utf8')
    return text


def to_string(text):
    """ 转成string"""
    if isinstance(text, bytes):
        text = text.decode('utf8', 'ignore')
    return text


def line_to_camel(text):
    """ 驼峰"""
    pattern = re.compile(r'(_\w)')
    sub = re.sub(pattern, lambda _map: _map.group(1)[1].upper(), text)
    return sub


def camel_to_line(text):
    """ 下划线"""
    pattern = re.compile(r'([a-z]|\d)([A-Z])')
    sub = re.sub(pattern, r'\1_\2', text).lower()
    return sub


def make_excel(title, headers, datas, filename='info.xls'):
    """ 创建excel"""
    wb = xlwt.Workbook()
    ws = wb.add_sheet(title)
    for idx, header in enumerate(headers):
        ws.write(0, idx, header)

    for row, data in enumerate(datas, 1):
        for col, d in enumerate(data):
            ws.write(row, col, d)
    
    if not os.path.exists(DOWN_DIR):
        os.mkdir(DOWN_DIR)
    path = os.path.join(DOWN_DIR, filename)
    wb.save(path)
    return path


def typeassert(func):
    """ 类型检测
    
    ＠typeassert
    def hello(x: int, y: str) -> list:
        ret = [x, y]
        return ret
    """
    sig = signature(func)
    annotations = func.__annotations__
    return_type = annotations.pop('return', None)
    bound_types = sig.bind_partial(**annotations).arguments
    @wraps(func)
    def wrapper(*args, **kw):
        bound_values = sig.bind(*args, **kw)
        for name, value in bound_values.arguments.items():
            if name in bound_types:
                if not isinstance(value, bound_types[name]):
                    raise TypeError(
                        "Argument '{}' must be {}".format(name, bound_types[name])
                    )
        
        ret = func(*args, **kw)
        if return_type:
            if not isinstance(ret, return_type):
                raise TypeError(
                    "Return Type must be {}".format(return_type)
                )
        return ret
    return wrapper


def url_route(url):
    """ 解析url 并生成oss相对路径"""
    route = re.sub(r'(http.*?\.com/)', '', url)
    return route

if __name__ == '__main__':
    print(camel_to_line('hello'))