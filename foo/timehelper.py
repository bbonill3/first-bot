from dateutil import parser as dateparser
from datetime import datetime
import re

MONTHS = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December']

def convert_user_datestring_to_datetime(datestring):
    if datestring.lower() == 'today':
        return datetime.now()
    else:
        return dateparser.parse(datestring)

def month_number(monthstr):
    return MONTHS.index(monthstr) + 1

def get_month_numbers(monthstr_1, monthstr_2):
    start_month = month_number(monthstr_1)
    end_month = month_number(monthstr_2)

    if start_month <= end_month: # e.g. March to November, 3 to 11
        return list(range(start_month, end_month + 1))
    else:  # e.g. October to March, 10 to 3, e.g. 10, 11, 12, 1, 2, 3
        start = list(range(start_month, 12 + 1)) # [10, 11, 12]
        end = list(range(1, end_month + 1)) # [1, 2, 3]
        return start + end

def is_month_in_range(monthstr, monthrangestr):
    """
    monthstr = 'March'
    monthrangestr could be 'Year Round', or 'March', or 'March - December', or 'May - December'
    """
    if monthrangestr == 'Year Round':
        return True
    else:
        mths = re.search('(\w+).+?(\w+)', monthrangestr).groups()
        target_month = month_number(monthstr)
        return target_month in get_month_numbers(mths[0], mths[1])


def get_market_hours_for_day_and_month(daystr, monthstr, market):
    d = {}
    if daystr in market['Open Days 1'] and is_month_in_range(monthstr, market['Open Months 1']):
        d['hours'] = market['Open Hours 1']
        d['days'] = market['Open Days 1']
        d['months'] = market['Open Months 1']
        return d
    elif daystr in market['Open Days 2'] and is_month_in_range(monthstr, market['Open Months 2']):
        d['hours'] = market['Open Hours 2']
        d['days'] = market['Open Days 2']
        d['months'] = market['Open Months 2']

        return d
    else:
        return False
