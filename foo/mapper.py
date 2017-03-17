import re
import requests

def get_latlngs(loc_string):
    s = re.search('37\.\d+, -122\.\d+', loc_string).group()
    latlng_string = s.replace(" ", "")
    return latlng_string

def make_locator_map(pointsonmap):
    GOOGLE_URL = 'https://maps.googleapis.com/maps/api/staticmap'
    myreq = requests.PreparedRequest()
    myreq.prepare_url(GOOGLE_URL, params={'size':'600x400', 'markers': pointsonmap})
    return myreq.url
