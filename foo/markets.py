import csv
import requests

DATA_URL = 'https://data.smcgov.org/api/views/ehqe-kh4j/rows.csv'

def make_data():
    resp = requests.get(DATA_URL)
    txt = resp.text
    lines = txt.splitlines()
    return list(csv.DictReader(lines))
