import requests
from bs4 import BeautifulSoup
import newspaper

def get_entry_urls(url):
    soup = BeautifulSoup(requests.get(url).textf)

    def get_row_entries(row_class):
        return list(map(lambda x: x.td.a['href'], soup.find_all("tr", {'class': row_class})))
    # get the even and odd entries in the table of biases
    return get_row_entries('odd').extend(get_row_entries('even'))


def get_site_link(site_subsections):
    soup = BeautifulSoup(requests.get("https://www.allsides.com/" + site_subsections))
    return soup.find_all("div", {'class': 'source-image'})[0].a['href']

start_url = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&title=&page='

start_ind = 0
site_subsections = []
while (True):
    subsection = get_entry_urls(start_url + str(start_ind))
    if len(subsection):
        site_subsections.extend(subsection)
    else:
        break

site_urls = [get_site_link(sub) for sub in site_subsections]

print(site_urls)