#!/usr/bin/env python3
import os
import pickle
import csv
import newspaper
import sys
import time
import json
from concurrent.futures import as_completed, ThreadPoolExecutor
from queue import Queue, Empty

def load_real(real_data, output_to):
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

    counter = 0

    def build_articles(paper):
        def aux():
            paper.build()
            for a in paper.articles:
                try:
                    a.download()
                    a.build()
                except Exception as e:
                    print(e)
        return aux

    def save_article(a):
        return {
            "url": a.url,
            "source_url": a.source_url,
            "text": a.text,
            "html": str(a.html),
            "tags": a.tags,
            "summary": a.summary,
            "keywords": a.keywords
        }



    futures = newspaper.news_pool.set(papers, fun=lambda x: build_articles(x))
    for nxt in as_completed(futures):
        for ar in futures[nxt].articles:
            if ar.download_exception_msg:
                print("LOOK======================================================")
                print(ar.download_exception_msg)
                print("END LOOK==================================================")
            else:
                print("Article !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                with open(os.path.join(output_to, str(counter) + ".pickle"), "wb+") as f:
                    counter += 1
                    pickler = pickle.Pickler(f)
                    pickler.fast = True
                    pickler.dump(save_article(ar))

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
            load_real(json.load(real), sys.argv[3])
            # load_fake(fake)
    print("Done!")
