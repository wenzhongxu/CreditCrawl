# -*- coding: utf-8 -*-
# @Time    : 2018/7/21 14:05
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : formatdate.py
# @Version : 1.0.1
# @Software: PyCharm
# @summary: 2018-6-21、2018年6月21、2018/6/21、21st Jun,2018、Jun 21st,2018（如果是其他月份还有缩写的形式）、
# Jun 21，2018、21-22 Jun 2018、Jun 21-22,2018、Thursday,21 Jun 2018（星期也可能会有缩写）

import re


class DateFormatHelper(object):
    regex1 = re.compile(r"\d{1,2}-\d{1,2} *[A-Za-z]+ *\d{4}")  # 21-22 Jun 2018
    regex2 = re.compile(r"\d{1,2} *[A-Za-z]+ *\d{4}")  # 21 Jun 2018
    regex3 = re.compile(r"\d{4}-\d{1,2}-\d{1,2}")  # 2018-6-21
    regex4 = re.compile(r"[A-Za-z]+ *\d{1,2}, *\d{4}")
    regex5 = re.compile(r"[A-Za-z]+ *\d{1,2}-\d{1,2}, *\d{4}")
    regex6 = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日.*?\d{2}:\d{2}")
    dateformatregexs = [regex1, regex2, regex3, regex4, regex5, regex6]

    monthMap = {"sep": "9", "oct": "10", "nov": "11", "dec": "12", "jan": "1", "feb": "2",
                "aug": "8", "jul": "7", "jun": "6", "may": "5", "apr": "4", "mar": "3"}
    monthMap2 = {"September": "9", "October": "10", "November": "11", "December": "12",
                 "January": "1", "February": "2", "August": "8", "July": "7",
                 "June": "6", "May": "5", "April": "4", "March": "3"}

    @classmethod
    def convertstandarddateformat(cls, datestr):
        """
        转换日期格式
        :param datestr:
        :return:
        """
        res = ""
        if datestr is None:
            return res
        datestr = str(datestr)
        for i in range(0, len(cls.dateformatregexs)):
            try:
                regex = cls.dateformatregexs[i]
                match = regex.match(datestr)
                if match is not None:
                    itemstr = match.group()
                    if i == 0:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[1]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[1]))
                        dayrange = str(items[0])
                        day = dayrange[0:dayrange.index("-")]
                        # day2 = dayrange[dayrange.index("-") + 1:]
                        res = year + "-" + month + "-" + day
                        # res2 = year + "-" + month + "-" + str(day2)
                    elif i == 1:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[1]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[1]))
                        day = items[0]
                        res = year + "-" + month + "-" + day
                    elif i == 2:
                        items = str(itemstr).split("-")
                        year = items[0]
                        month = items[1]
                        day = items[2]
                        if len(year) == 2:
                            year = "20" + year
                        if len(month) == 1:
                            month = "0" + month
                        if len(day) == 1:
                            day = "0" + day
                        res = year + "-" + month + "-" + day
                    elif i == 3:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[0]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[0]))
                        digit_pattern = re.compile(r'[0-9]+')
                        digitlist = digit_pattern.findall(items[1])
                        day = digitlist[0]
                        res = year + "-" + month + "-" + day
                    elif i == 4:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[0]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[0]))
                        dayrange = str(items[1])
                        day = dayrange[0:dayrange.index("-")]
                        # day2 = dayrange[dayrange.index("-")+1:dayrange.index(",")]
                        res = year + "-" + month + "-" + day
                        # res2 = year + "-" + month + "-" + day2
                    elif i == 5:
                        itemstr = itemstr.decode('utf-8')
                        for x in range(len(itemstr)):
                            if ord(itemstr[x]) > 255:
                                itemstr = itemstr.replace(itemstr[x], " ")
                        # items = str(itemstr.encode('gbk')).split(" ")
                        items = str(itemstr).split(" ")
                        year = items[0]
                        month = items[1]
                        day = items[2]
                        res = year + "-" + month + "-" + day + " " + items[3]
                    else:
                        res = datestr
                    print(res)
                    break
            except Exception as e:
                print("日期统一格式化方法出现异常{}".format(e))
        return res


if __name__ == '__main__':
    # DateFormatHelper().convertstandarddateformat("2017年12月21日 12:23")
    # DateFormatHelper().convertstandarddateformat("2017年12月21日")
    # DateFormatHelper().convertstandarddateformat("2018-6-21 12:34")
    resss = DateFormatHelper().convertstandarddateformat(u'2018年07月30日13:26')
    print resss
