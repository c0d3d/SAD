#1/usr/bin/env python3

import newspaper
import sys
import time
import json

def run(real_data, fake_data):
    for paper_url in real_data:
        paper = newspaper.build(paper_url['source-url'])
        for art in paper.articles:
            art.download()
            print(art.url)
    # print("Setting papers", papers)
    # newspaper.news_pool.set(papers)
    # print("Joining ...")
    # newspaper.news_pool.join()
    # print("Should be done ...")
    # for a in papers:
    #     a.download()
    #     for ar in a.articles:
    #         print(ar.url)



if __name__ == "__main__":
    with open(sys.argv[1], "r") as real:
        with open(sys.argv[2], "r") as fake:
            run(json.load(real), json.load(fake))
    print("Done!")
