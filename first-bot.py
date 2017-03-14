import csv
from dateutil import parser as dateparser
from datetime import datetime
import re
import requests

DATA_URL = 'https://data.smcgov.org/api/views/ehqe-kh4j/rows.csv'

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

def make_data():
    resp = requests.get(DATA_URL)
    txt = resp.text
    lines = txt.splitlines()
    return list(csv.DictReader(lines))

def get_latlngs(loc_string):
    s = re.search('37\.\d+, -122\.\d+', loc_string).group()
    latlng_string = s.replace(" ", "")
    return latlng_string

def make_locator_map(pointsonmap):
    GOOGLE_URL = 'https://maps.googleapis.com/maps/api/staticmap'
    myreq = requests.PreparedRequest()
    myreq.prepare_url(GOOGLE_URL, params={'size':'600x400', 'markers': pointsonmap})
    return myreq.url

def make_story(market, metainfo):
    storytemplate = "{name} is open on {monthname} {dayname}, {hours}. Here is a map of the market:{url}"

    market_points = get_latlngs(market['Location 1'])
    google_map_url = make_locator_map(market_points )

    story = storytemplate.format(
        name=market['Market Name'],
        dayname=metainfo['days'],
        hours=metainfo['hours'],
        monthname=metainfo['months'],
        url=google_map_url)
    return story

def bot(datestr='Today'):
    thedate = convert_user_datestring_to_datetime(datestr)

    the_weekday =  thedate.strftime('%A')
    the_month_name =  thedate.strftime('%B')

    print("Hello, checking for markets open on", the_weekday + 's', 'in', the_month_name)
    markets = make_data()
    for market in markets:
        md = get_market_hours_for_day_and_month(the_weekday, the_month_name, market)
        if md:
            story = make_story(market, md)
            print(story)

if __name__ == '__main__':
    bot()
