# 1/usr/bin/env python3
import csv
import newspaper
import sys
import time
import json

def load_real(real_data):
    papers = []
    for paper_url in real_data:
        print("Pre", paper_url['source-url'])
        paper = newspaper.build(paper_url['source-url'],
                                browser_user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0)',
                                verbose=True,
                                timeout=250,
                                dry=True,
                                memoize_articles=False)
        print(paper_url, paper)
        papers.append(paper)
#            paper.download()
#            for art in paper.articles:
#                time.sleep(.01)
#                print(paper_url['source-url'], art.url)
#                out.write('{}\t{}\n'.format(paper_url['source-url'], art.url))

    print("Setting papers!")
    newspaper.news_pool.set_papers(papers)
    print("Joining ...")
    try:
        while True:
            nxt = newspaper.news_pool.next_done()
            nxt.print_summary()
            for ar in nxt.articles:
                print("Article URL", ar.url)
    except Exception:
        print("No more papers!")

    print("Should be done ...")


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
