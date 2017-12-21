#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 8:49
# @Author  : Aries (i@iw3c.com)
# @Site    : http://iw3c.com
# @File    : transfer.py
# @Software: PyCharm
import os
import time
import copy
from wox import Wox, WoxAPI
result_template = {
    'Title': '{}:{}',
    'SubTitle': '点击复制到剪贴板',
    'IcoPath': 'ui/icon.png',
    'JsonRPCAction': {
        'method': 'copy_to_clipboard',
        'parameters': ['{}'],
        'dontHideAfterAction': False
    }
}


class Main(Wox):
    def query(self, key):
        result = []
        param = key.strip()
        if param == 'now':
            param = int(time.time())
            local_time = time.localtime(param)
            time_result = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            unix_format = copy.deepcopy(result_template)
            unix_format['Title'] = unix_format['Title'].format('当前时间：', param)
            unix_format['JsonRPCAction']['parameters'][0] = unix_format['JsonRPCAction']['parameters'][0].format(param)
            result.append(unix_format)
        else:
            unix_time = self.is_unixtime(param)
            if unix_time is False:
                if ":" in param:
                    time_data = time.strptime(param, "%Y-%m-%d %H:%M:%S")
                else:
                    time_data = time.strptime(param, "%Y-%m-%d")
                time_result = int(time.mktime(time_data))
            else:
                local_time = time.localtime(unix_time)
                time_result = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        result_template['Title'] = '转换结果：%s' % (time_result,)
        result_template['JsonRPCAction']['parameters'][0] = time_result
        result.append(result_template)
        return result

    def copy_to_clipboard(self, value):
        command = 'echo ' + str(value).strip() + '| clip'
        os.system(command)

    def is_unixtime(self, value):
        try:
            strlen = len(value)
            '''支持10位或者13位unixtime'''
            if strlen != 10 and strlen != 13:
                raise Exception('时间格式错误')
            data = int(value)
            if strlen == 13:
                data = data / 1000.0
            return data
        except:
            return False


if __name__ == '__main__':
    Main()