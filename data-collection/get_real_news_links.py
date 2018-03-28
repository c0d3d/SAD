#!/usr/bin/env python3

from bs4 import BeautifulSoup
from enum import Enum
import newspaper
import requests
import time

class BiasRating(Enum):
    Left      = 1
    LeanLeft  = 2
    Center    = 3
    LeanRight = 4
    Right     = 5
    All       = 6

    @staticmethod
    def from_string(s):
        s = s.upper()
        if s == "LEFT":
            return BiasRating.Left
        elif s == "LEFT-CENTER":
            return BiasRating.LeanLeft
        elif s == "CENTER":
            return BiasRating.Center
        elif s == "RIGHT-CENTER":
            return BiasRating.LeanRight
        elif s == "RIGHT":
            return BiasRating.Right
        elif s == "ALLSIDES":
            return BiasRating.All
        else:
            raise Exception("unkown bias: %s" % s)


def get_entry_urls(url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    selectors = [
        # href for source
        soup.select("td.views-field.source-title a"),
        # href for image
        soup.select("td.views-field.views-field-field-bias-image a"),
        # Agree count
        soup.select("td.views-field.community-feedback div div.rate-details span.agree"),
        # Disagree count
        soup.select("td.views-field.community-feedback div div.rate-details span.disagree")
    ]

    output = []
    for selector in zip(*selectors):
        bias_str = selector[1]['href']
        bias_str = bias_str[bias_str.rfind('/')+1:]
        output.append({
            "source-url" : selector[0]['href'],
            "source-name" : selector[0].text,
            "source-bias" : BiasRating.from_string(bias_str),
            "source-score": (int(selector[2].text), int(selector[3].text))
        })
    return output

def get_site_link(sub_url):
    soup = BeautifulSoup(requests.get("https://www.allsides.com/" + sub_url).text, "lxml")
    return soup.find_all("div", {'class': 'source-image'})[0].a['href']

start_url = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&title=&page='

if __name__ == "__main__":
    for i in range(4):
        for e in get_entry_urls(start_url + str(i)):
            print(e)
