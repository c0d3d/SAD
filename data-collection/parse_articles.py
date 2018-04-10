# 1/usr/bin/env python3
import csv
import newspaper
import sys
import time
import pandas as pd


def parse(out, url_file, real):
    out.write('{}\t{}\t'.format('site', 'url', 'title', 'body', 'date', 'fake'))
    reader = csv.reader(url_file, delimiter='\t')
    print(get_k_value(url_file))
    return 1
    for site, url in reader:
        time.sleep(.1)
        article = newspaper.Article(url)
        article.download()
        article.parse()
        fake = 0 if real else 1
        out.write('{}\t{}\t{}\t{}\t{}\t{}'.format(site,
                                                  url,
                                                  article.title,
                                                  article.text,
                                                  article.publish_date,
                                                  fake))


def get_k_value(url_file):
    url_df = pd.read_csv(url_file, sep='\t', error_bad_lines=False,
                         header=None, names=['url', 'article_url'])
    url_counts = url_df.groupby(['url']).count().drop_index()
    opt = 0
    max_count = 0
    max_num_articles = url_counts['article_url'].max()
    for i in range(max_num_articles):
        num_sites = url_counts[url_counts['article_url'] > i].shape[0]
        count = num_sites * i
        if count > max_count:
            opt = i
            max_count = count
    return opt


if __name__ == "__main__":
    with open(sys.argv[1], "r") as real:
        with open(sys.argv[2], "r") as fake:
            with open(sys.argv[3], "w+") as out:
                parse(out, real, real=True)
                parse(out, fake, real=False)
    print("Done!")
