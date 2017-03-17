from datetime import datetime
from foo.timehelper import convert_user_datestring_to_datetime, get_market_hours_for_day_and_month
from foo.markets import make_data
from foo.stories import make_story

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
