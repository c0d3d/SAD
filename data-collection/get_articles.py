# 1/usr/bin/env python3
import csv
import newspaper
import sys
import time
import json
import requests


def load_real(real_data):
    with open("articles_2.txt", 'w') as out:
        for paper_url in real_data:
            time.sleep(.01)
            # print(paper_url['source-url'])
            paper = newspaper.build(paper_url['source-url'],
                                    proxies={'http': 'http://127.0.0.1:9150',
                                             'https': 'https://127.0.0.1:9151'},
                                    browser_user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0)',
                                    memoize_articles=False,
                                    follow_meta_refresh=True,
                                    verbose=True)
            paper.download()
            for art in paper.articles:
                time.sleep(.01)
                print(paper_url['source-url'], art.url)
                out.write('{}\t{}\n'.format(paper_url['source-url'], art.url))

    # print("Setting papers", papers)
    # newspaper.news_pool.set(papers)
    # print("Joining ...")
    # newspaper.news_pool.join()
    # print("Should be done ...")
    # for a in papers:
    #     a.download()
    #     for ar in a.articles:
    #         print(ar.url)


def load_fake(fake):
    with open("fake.txt", 'w') as out:
        reader = csv.reader(fake, delimiter=',')
        for row in reader:
            time.sleep(.01)
            url = 'http://' + row[0]
            paper = newspaper.build(url)
            for art in paper.articles:
                time.sleep(.01)
                out.write('{}\t{}\n'.format(url, art.url))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as real:
        with open(sys.argv[2], "r") as fake:
            load_real(json.load(real))
            # load_fake(fake)
    print("Done!")
