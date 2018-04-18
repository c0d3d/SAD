#!/usr/bin/env python3
import pickle
import sys

def dump_article(path, key):
    with open(path, "rb") as f:
        article = pickle.load(f)
        print(article[key])

if __name__ == "__main__":
    dump_article(sys.argv[1], "text" if len(sys.argv) == 2 else sys.argv[2])
