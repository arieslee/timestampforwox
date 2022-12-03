#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 8:49
# @Author  : Aries (i@iw3c.com)
# @Site    : http://iw3c.com
# @File    : transform.py
# @Software: PyCharm
import os
import time
import copy
from wox import Wox, WoxAPI
from datetime import datetime, timedelta, timezone
result_template = {
    'Title': '{}: {}',
    'SubTitle': 'copy to clipboard',
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
        query_time = param

        aimed_timezone_offset = 0
        param_split = param.split(' ', 1)
        is_aimed_timezone = len(param_split) == 2 and param_split[0].startswith('utc')
        if is_aimed_timezone:
            aimed_timezone_str = param_split[0]
            if len(aimed_timezone_str) > 3:
                aimed_timezone_offset = int(aimed_timezone_str[3:])
            query_time = param_split[1]

        if query_time == 'now' or (is_aimed_timezone and param_split[1] == 'now'):
            local_time = datetime.now()
            query_time = int(local_time.timestamp())
            time_result = self.format_timestamp(query_time, is_aimed_timezone, aimed_timezone_offset)

            unix_format = copy.deepcopy(result_template)
            unix_format['Title'] = unix_format['Title'].format('now', query_time)
            unix_format['JsonRPCAction']['parameters'][0] = unix_format['JsonRPCAction']['parameters'][0].format(query_time)
            result.append(unix_format)
        else:
            unix_time = self.is_unixtime(query_time)
            if unix_time is False:
                if ":" in query_time:
                    time_data = datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")
                else:
                    time_data = datetime.strptime(query_time, "%Y-%m-%d")
                if is_aimed_timezone:
                    time_data = time_data.replace(tzinfo=timezone(timedelta(hours=aimed_timezone_offset)))
                    time_result = time_data.timestamp()
                else:
                    time_result = time_data.timestamp()
            else:
                time_result = self.format_timestamp(unix_time, is_aimed_timezone, aimed_timezone_offset)

        result_template['Title'] = 'result: %s' % (time_result,)
        result_template['JsonRPCAction']['parameters'][0] = time_result
        result.append(result_template)
        return result

    def format_timestamp(self, timestamp, is_aimed_timezone, aimed_timezone_offset):
        tz_aimed = timezone(timedelta(hours=aimed_timezone_offset))
        if is_aimed_timezone:
            time_result = datetime.fromtimestamp(timestamp, tz_aimed).strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_result = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return time_result

    def copy_to_clipboard(self, value):
        command = 'echo ' + str(value).strip() + '| clip'
        os.system(command)

    def is_unixtime(self, value):
        try:
            strlen = len(value)
            '''support 10 or 13 length unixtime |支持10位或者13位unixtime'''
            if strlen != 10 and strlen != 13:
                raise Exception('timestamp format error')
            data = int(value)
            if strlen == 13:
                data = data / 1000.0
            return data
        except:
            return False


if __name__ == '__main__':
    Main()