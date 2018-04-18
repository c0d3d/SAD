#!/usr/bin/env python3

from bs4 import BeautifulSoup
from enum import Enum
import newspaper
import requests
import time
import json
import sys

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
        if s == "RIGHT" \
           or s == "ALLSIDES" \
           or s == "RIGHT-CENTER" \
           or s == "CENTER" \
           or s == "LEFT-CENTER" \
           or s == "LEFT":
            return s
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

    for selector in zip(*selectors):
        bias_str = selector[1]['href']
        bias_str = bias_str[bias_str.rfind('/') + 1:]
        yield {
            "source-url" : selector[0]['href'],
            "source-name" : selector[0].text,
            "source-bias" : BiasRating.from_string(bias_str),
            "source-score": (int(selector[2].text), int(selector[3].text))
        }

def get_site_link(sub_url, name):
    soup = BeautifulSoup(requests.get("https://www.allsides.com/" + sub_url).text, "lxml")
    ans = soup.select("div.span4.source-image-wrapper.News.Media div.source-image a")[0]['href']
    if ans == "http:// ":
        for x in soup.select(
                "article.node.node-news-source div.row-fluid.field.field-name-body.field-type-text-with-summary div.field-items p a"):
            if name in x.text:
                return x['href']
    else:
        return ans

start_url = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&title=&page='

if __name__ == "__main__":
    output = []
    for i in range(4):
        for e in get_entry_urls(start_url + str(i)):
            e['source-url'] = get_site_link(e['source-url'], e['source-name'])
            if e['source-url'] is None:
                continue
            else:
                e['source-url'] = e['source-url'].strip().rstrip('/')
            output.append(e)
            time.sleep(0.15)
    json.dump(output, sys.stdout)
