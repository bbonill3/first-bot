from foo.mapper import get_latlngs, make_locator_map

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
