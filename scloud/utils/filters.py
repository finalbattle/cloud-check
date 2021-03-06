#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import re
from datetime import datetime
from scloud.config import logger
import urllib2


class Filters(object):
    @classmethod
    def init(cls, env):
        method_prefix = 'filter_'
        flts = Filters()
        methods = dir(flts)
        for m in methods:
            if not m.startswith(method_prefix): continue
            fname = m[len(method_prefix):]
            env.filters[fname] = flts.__getattribute__(m)

    def filter_urlquote(self, value):
        return urllib2.quote(value)

    def filter_urlunquote(self, value):
        return urllib2.unquote(value)

    def filter_getGoodTime(self, time_str):
        logger.info(time_str)
        if not time_str:
            return ""
        if isinstance(time_str, datetime):
            t = time_str
        else:
            t = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        retstr = ''
        if not t: return u'N/A'
        if datetime.now() < t: return u'N/A'
        delta = datetime.now() - t
        if delta.days >= 30: retstr = t.strftime('%Y-%m-%d')
        elif delta.days >= 1: retstr = u'%d天前' % (delta.days)
        elif delta.seconds < 60: retstr = u'刚刚'
        elif delta.seconds < 3600: retstr = u'%d分钟前' % (delta.seconds / 60)
        elif delta.seconds < 86400: retstr = u'%d小时前' % (delta.seconds / 3600)
        else: retstr = u'%d小时前' % (delta.seconds / 3600)
        return retstr

    def filter_getGoodTimeLevel(self, time_str):
        logger.info(time_str)
        if not time_str:
            return ""
        if isinstance(time_str, datetime):
            t = time_str
        else:
            t = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        level = ''
        if not t: return u'N/A'
        if datetime.now() < t: return u'N/A'
        delta = datetime.now() - t
        if delta.days >= 30: level = 'danger'
        elif delta.days >= 1: level = 'warning'
        elif delta.seconds < 60: level = 'info'
        elif delta.seconds < 3600: level = 'success'
        elif delta.seconds < 86400: level = 'primary'
        else: level = 'primary'
        return level

    def filter_format_datetime(self, time_str):
        if time_str:
            if type(time_str) == "str":
                t = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            else:
                t = time_str
            retstr = ''
            if not t: return u'N/A'
            if t >= datetime.strptime("9999-12-31 23:59:59", "%Y-%m-%d %H:%M:%S"):
                return ''
            return t.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ''

    def filter_status_filter(self, values, status=0):
        values = [i for i in values if i.status == status]
        return values

    def filter_status_list(self, STATUS, reverse=False):
        values = [STATUS.get(i) for i in STATUS.keys() if isinstance(i, int)]
        if reverse:
            values = values[::-1]
        return values

    def filter_is_number(self, value):
        return str(value).isdigit()

    def filter_filter_s(self, value, reg=''):
        # from code import interact
        # interact(local=locals())
        find_list = re.compile(reg).findall(value)
        logger.info(find_list)
        for key in find_list:
            logger.info(key)
            value = value.replace(key, '')
            logger.info(value)
        return value
