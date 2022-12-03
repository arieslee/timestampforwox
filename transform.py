#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 8:49
# @Author  : Aries (i@iw3c.com), KTY
# @Site    : http://iw3c.com
# @File    : transform.py
# @Software: PyCharm
import os
import copy
from typing import List
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
        query_time, _timezone = self.parse_input(key)

        if query_time == 'now':
            now_timestamp = int(datetime.now().timestamp())
            self.append_timestamp_result(result, now_timestamp)
            time_result = self.format_timestamp(now_timestamp, _timezone)
            self.append_datetime_result(result, time_result)
        elif self.is_timestamp(query_time):
            query_timestamp = self.parse_timestamp(query_time)
            time_result = self.format_timestamp(query_timestamp, _timezone)
            self.append_datetime_result(result, time_result)
        else:
            if ":" in query_time:
                time_data = datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")
            else:
                time_data = datetime.strptime(query_time, "%Y-%m-%d")
            time_data = time_data.replace(tzinfo=_timezone)
            time_result = int(time_data.timestamp())
            self.append_timestamp_result(result, time_result)

        return result

    def append_datetime_result(self, result: List[dict], time_result: str):
        result_template['Title'] = 'datetime: %s' % (time_result,)
        result_template['JsonRPCAction']['parameters'][0] = time_result
        result.append(result_template)

    def append_timestamp_result(self, result: List[dict], timestamp: int):
        unix_format = copy.deepcopy(result_template)
        unix_format['Title'] = unix_format['Title'].format('timestamp', timestamp)
        unix_format['JsonRPCAction']['parameters'][0] = str(timestamp)
        result.append(unix_format)

    def parse_input(self, key: str) -> (str, timezone):
        input = key.strip()
        params = input.split(' ', 1)
        is_set_timezone = len(params) == 2 and params[0].startswith('utc')
        if is_set_timezone:
            aimed_timezone_str = params[0]
            aimed_timezone_offset = 0
            if len(aimed_timezone_str) > 3:
                aimed_timezone_offset = int(aimed_timezone_str[3:])
            used_timezone = timezone(timedelta(hours=aimed_timezone_offset))
            query_time = params[1]
        else:
            used_timezone = None
            query_time = input
        return query_time, used_timezone

    def format_timestamp(self, timestamp: int, _timezone: timezone) -> str:
        return datetime.fromtimestamp(timestamp, tz=_timezone).strftime("%Y-%m-%d %H:%M:%S")

    def copy_to_clipboard(self, value):
        command = 'echo ' + str(value).strip() + '| clip'
        os.system(command)

    def is_timestamp(self, value: str) -> bool:
        strlen = len(value)
        '''support 10 or 13 length unixtime |支持10位或者13位unixtime'''
        if strlen != 10 and strlen != 13:
            return False
        try:
            int(value)
        except:
            return False
        return True

    def parse_timestamp(self, value: str) -> int:
        data = int(value)
        strlen = len(value)
        if strlen == 13:
            data = data / 1000.0
        return data


if __name__ == '__main__':
    Main()
