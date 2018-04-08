# 1/usr/bin/env python3
import csv
import newspaper
import sys
import time


def parse(url_file, real):
    out_file = 'real.tsv' if real else 'fake.tsv'
    with open(out_file, 'w') as out:
        out.write('{}\t{}\t'.format('site', 'url', 'title', 'body', 'date', 'fake'))
        reader = csv.reader(url_file, delimiter='\t')
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


if __name__ == "__main__":
    with open(sys.argv[1], "r") as real:
        with open(sys.argv[2], "r") as fake:
            parse(real, real=True)
            parse(fake, real=False)
    print("Done!")
